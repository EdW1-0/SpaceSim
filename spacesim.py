import pygame
from gameModel import GameModel
from views.menuContext import MenuContext

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

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





def main():
    pygame.init()

    gameModel = GameModel()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    menuContext = MenuContext(screen, gameModel)

    running = True
    while running:
        
        outerEvent = menuContext.run()
        
        if outerEvent == QUIT:
            running = False
        

        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    print("Launching spacesim")
    main()