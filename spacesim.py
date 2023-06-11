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
from views.orbitContext import LOADMENUVIEW
from views.surfaceContext import LOADSURFACEVIEW, LOADCOLONYVIEW, SCMode





def main():
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

            if "mode" in guiContext.upperContext:
                mode = guiContext.upperContext["mode"]
            else:
                mode = SCMode.Standard
            
            manager.clear_and_reset()
            guiContext = SurfaceContext(screen, gameModel, manager, planet, mode=mode)
        
        elif outerEvent == LOADCOLONYVIEW:
            if "colony" not in guiContext.upperContext:
                print("Invalid state - tried to load colony view with no colony")
                assert(False)
            colonyId = guiContext.upperContext["colony"]
            colony = gameModel.colonySim.colonyById(colonyId)
            manager.clear_and_reset()
            guiContext = ColonyContext(screen, gameModel, manager, colony)

        
        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
    print("Launching spacesim")
    main()