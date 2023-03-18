import pygame

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
    QUIT,
)

def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                break

        screen.fill((135, 206, 250))

        pygame.draw.rect(screen, (10, 10, 10), pygame.Rect(200, 200, 100, 50))

        font = pygame.font.Font()
        text = font.render("Lorem Ipsum", True, (0, 0, 128))
        textRect = text.get_rect()
        textRect.center = (250, 225)

        screen.blit(text, textRect)

        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    print("Launching spacesim")
    main()