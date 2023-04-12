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

LOADSURFACEVIEW = pygame.USEREVENT + 3

class SurfaceContext(GUIContext):
    def __init__(self, screen, model, manager):
        super(SurfaceContext, self).__init__(screen, model, manager)

    def run(self):
        returnCode = 0

        for event in pygame.event.get():
            if event.type == QUIT:
                returnCode = QUIT
                break

        self.screen.fill((200, 135, 250))

        return returnCode