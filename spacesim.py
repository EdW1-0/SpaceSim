import pygame
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

    guiContext = None
    gameModel = GameModel()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    guiContext = MenuContext(screen, gameModel)

    running = True
    while running:
        
        outerEvent = guiContext.run()
        
        if outerEvent == QUIT:
            running = False
        elif outerEvent == LOADORBITVIEW:
            guiContext = OrbitContext(screen, gameModel)
        elif outerEvent == LOADMENUVIEW:
            guiContext = MenuContext(screen, gameModel)
        

        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    print("Launching spacesim")
    main()