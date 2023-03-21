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
    MOUSEBUTTONUP,
    QUIT,
)

class MenuItem(pygame.sprite.Sprite):
    def __init__(self, center=(0, 0), text="Default", handler=None):
        super(MenuItem, self).__init__()
        self.text = text
        if (handler):
            self.handler = handler
        else:        
            self.handler = self.click
        self.surf = pygame.surface.Surface((100, 50))
        pygame.draw.rect(self.surf, (10, 10, 10), pygame.Rect(0, 0, 100, 50))
        

        font = pygame.font.Font(size=20)
        text = font.render(self.text, True, (128, 128, 230))
        textRect = text.get_rect()
        textRect.center = (50, 25)

        self.surf.blit(text, textRect)

        self.rect = self.surf.get_rect(center=center)

    def click(self):
        print (self.text)


def quitHandler():
    print("Quitting...")
    pygame.event.post(pygame.event.Event(QUIT))


def loadHandler():
    print("Loading...")


def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    loadItem = MenuItem((200, 100), text="Load Game", handler=loadHandler)
    quitItem = MenuItem((200, 200), text="Quit Game", handler=quitHandler)

    all_sprites = pygame.sprite.Group()
    all_sprites.add(loadItem)
    all_sprites.add(quitItem)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                break
            elif event.type == MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()

                clicked_items = [s for s in all_sprites if s.rect.collidepoint(pos)]
                for c in clicked_items:
                    c.handler()

        screen.fill((135, 206, 250))

        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    print("Launching spacesim")
    main()