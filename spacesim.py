import pygame
import pygame_gui

from gameModel import GameModel
from views.menuContext import MenuContext
from views.orbitContext import OrbitContext
from views.surfaceContext import SurfaceContext
from views.colonyContext import ColonyContext

# Define constants for the screen width and height
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    MOUSEBUTTONUP,
    QUIT,
)

from views.orbitContext import OCMode
from views.surfaceContext import SCMode

from views.guiContext import GUICode


def main(testingCallback = None):
    pygame.init()

    manager = pygame_gui.UIManager((1200, 800))

    guiContext = None
    gameModel = GameModel()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    guiContext = MenuContext(screen, gameModel, manager)

    clock = pygame.time.Clock()

    running = True
    while running:
        time_delta = clock.tick(60)/1000.0

        gameModel.tick()

        outerEvent = guiContext.run()
        
        if outerEvent == QUIT:
            running = False
        
        elif outerEvent == GUICode.LOADORBITVIEW:
            manager.clear_and_reset()
            if isinstance(guiContext, SurfaceContext) and hasattr(guiContext, "upperContext") and "node" in guiContext.upperContext:
                # Return from surface after setting surface target for ship
                landingContext = {
                    "ship": guiContext.upperContext["ship"],
                    "target": guiContext.upperContext["node"],
                    "surfaceCoordinates": guiContext.upperContext["surfaceCoordinates"]
                }
                guiContext = OrbitContext(screen, gameModel, manager, mode = OCMode.Target, landingContext = landingContext)
            elif isinstance(guiContext, ColonyContext):
                # Launch planning from colony
                landingContext = {
                    "ship": guiContext.upperContext["ship"],
                    "colony": guiContext.upperContext["colony"]
                }
                guiContext = OrbitContext(screen, gameModel, manager, mode = OCMode.LaunchPlan, landingContext =landingContext)
            elif isinstance(guiContext, SurfaceContext) and hasattr(guiContext, "upperContext"):
                # Launch planning from surface
                landingContext = guiContext.upperContext
                guiContext = OrbitContext(screen, gameModel, manager, mode = OCMode.LaunchPlan, landingContext =landingContext)
            else:
                # Direct access
                guiContext = OrbitContext(screen, gameModel, manager)
        
        elif outerEvent == GUICode.LOADMENUVIEW:
            manager.clear_and_reset()
            guiContext = MenuContext(screen, gameModel, manager)
        
        elif outerEvent == GUICode.LOADSURFACEVIEW:
            if "planet" not in guiContext.upperContext:
                print("Invalid state - tried to load planet surface with no planet")
                assert(False)
            planetId = guiContext.upperContext["planet"]
            planet = gameModel.planetSim.planetById(planetId)
            manager.clear_and_reset()


            if isinstance(guiContext, OrbitContext):
                # Drop down to set target for landing
                if "mode" in guiContext.upperContext and guiContext.upperContext["mode"] == SCMode.Landing:
                    landingContext = {
                        "ship": guiContext.upperContext["ship"],
                        "planet": guiContext.upperContext["planet"],
                        "node": guiContext.upperContext["node"]
                    }
                    guiContext = SurfaceContext(screen, 
                                                gameModel, 
                                                manager, 
                                                planet, 
                                                mode=SCMode.Landing, 
                                                landingContext = landingContext)
                # Return from setting launch target for confirmation
                elif "mode" in guiContext.upperContext and guiContext.upperContext["mode"] == SCMode.Target:
                    landingContext = {
                        "ship": guiContext.upperContext["ship"],
                        "planet": guiContext.upperContext["planet"],
                        "trajectory": guiContext.upperContext["trajectory"]
                    }
                    guiContext = SurfaceContext(screen, gameModel, manager, planet, mode = SCMode.Target, landingContext = landingContext)
                # Direct access from OrbitContext
                else:
                    guiContext = SurfaceContext(screen, gameModel, manager, planet)

            # Direct access from ColonyContext
            elif isinstance(guiContext, ColonyContext):
                guiContext = SurfaceContext(screen, gameModel, manager, planet)
        
        elif outerEvent == GUICode.LOADCOLONYVIEW:
            if "colony" not in guiContext.upperContext:
                print("Invalid state - tried to load colony view with no colony")
                assert(False)
            colonyId = guiContext.upperContext["colony"]
            colony = gameModel.colonySim.colonyById(colonyId)
            manager.clear_and_reset()
            # Return to ColonyContext after setting launch target
            if "ship" and "trajectory" in guiContext.upperContext:
                launchContext = {
                    "ship": guiContext.upperContext["ship"],
                    "trajectory": guiContext.upperContext["trajectory"]
                }
            # Direct access from SurfaceContext
            else:
                launchContext = None
            guiContext = ColonyContext(screen, gameModel, manager, colony, launchContext = launchContext)

        
        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.update()

        if testingCallback:
            testingCallback(gameModel, guiContext)

    pygame.quit()

if __name__ == '__main__':
    print("Launching spacesim")
    main()