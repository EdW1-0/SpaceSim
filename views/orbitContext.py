from views.guiContext import GUIContext

import pygame

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

LOADMENUVIEW = pygame.USEREVENT + 2

class OrbitContext(GUIContext):
    def __init__(self, screen, model):
        super(OrbitContext, self).__init__(screen, model)
    
    def run(self):
        returnCode = 0

        for event in pygame.event.get():
            if event.type == QUIT:
                returnCode = QUIT
                break
            elif event.type == MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()

                if pos[0] < 50 and pos[1] < 50:
                    print ("foo")
                    returnCode = LOADMENUVIEW
                    break

        self.screen.fill((250, 206, 100))

        surf = pygame.surface.Surface((50, 50))
        pygame.draw.rect(self.screen, (10, 10, 10), pygame.Rect(0, 0, 50, 50))
     


        return returnCode