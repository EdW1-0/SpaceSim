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

from views.menuContext import LOADORBITVIEW
from views.orbitContext import LOADMENUVIEW, OCMode
from views.surfaceContext import LOADSURFACEVIEW, LOADCOLONYVIEW, SCMode





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
        
        elif outerEvent == LOADORBITVIEW:
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
        
        elif outerEvent == LOADMENUVIEW:
            manager.clear_and_reset()
            guiContext = MenuContext(screen, gameModel, manager)
        
        elif outerEvent == LOADSURFACEVIEW:
            if "planet" not in guiContext.upperContext:
                print("Invalid state - tried to load planet surface with no planet")
                assert(False)
            planetId = guiContext.upperContext["planet"]
            planet = gameModel.planetSim.planetById(planetId)
            manager.clear_and_reset()


            if isinstance(guiContext, OrbitContext):
                # 
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
                else:
                    guiContext = SurfaceContext(screen, gameModel, manager, planet)

            elif isinstance(guiContext, ColonyContext):
                guiContext = SurfaceContext(screen, gameModel, manager, planet)

                # if "ship" in guiContext.upperContext:
                # else:
                #     if "mode" in guiContext.upperContext:
                #         mode = guiContext.upperContext["mode"]
                #     else:
                #         mode = SCMode.Standard
                    
                #     if "ship" in guiContext.upperContext and "node" in guiContext.upperContext:
                #         landingContext = {"ship": guiContext.upperContext["ship"],
                #                         "node": guiContext.upperContext["node"]}
                #     elif "ship" in guiContext.upperContext and "trajectory" in guiContext.upperContext:
                #         landingContext = {
                #             "ship": guiContext.upperContext["ship"],
                #             "trajectory": guiContext.upperContext["trajectory"]
                #         }
                #     else:
                #         # Direct access
                #         landingContext = {}

                #     guiContext = SurfaceContext(screen, gameModel, manager, planet, mode=mode, landingContext = landingContext)
        
        elif outerEvent == LOADCOLONYVIEW:
            if "colony" not in guiContext.upperContext:
                print("Invalid state - tried to load colony view with no colony")
                assert(False)
            colonyId = guiContext.upperContext["colony"]
            colony = gameModel.colonySim.colonyById(colonyId)
            manager.clear_and_reset()
            if "ship" and "trajectory" in guiContext.upperContext:
                launchContext = {
                    "ship": guiContext.upperContext["ship"],
                    "trajectory": guiContext.upperContext["trajectory"]
                }
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