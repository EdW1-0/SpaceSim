import pygame
import pygame_gui

from gameModel import GameModel
from views.menuContext import MenuContext
from views.orbitContext import OrbitContext

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

        outerEvent = guiContext.run()
        
        if outerEvent == QUIT:
            running = False
        elif outerEvent == LOADORBITVIEW:
            manager.clear_and_reset()
            guiContext = OrbitContext(screen, gameModel, manager)
        elif outerEvent == LOADMENUVIEW:
            manager.clear_and_reset()
            guiContext = MenuContext(screen, gameModel, manager)
        
        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
    print("Launching spacesim")
    main()