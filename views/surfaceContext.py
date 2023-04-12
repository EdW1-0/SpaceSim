from views.guiContext import GUIContext

import pygame
import math

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


center = (500, 400)
radius = 300

class SurfaceContext(GUIContext):
    def __init__(self, screen, model, manager):
        super(SurfaceContext, self).__init__(screen, model, manager)
        self.surf = pygame.Surface((1200, 800))
        self.surf.fill((50, 50, 50))
        pxArray = pygame.surfarray.pixels3d(self.surf)
        shape = pxArray.shape
        for i in range(shape[0]):
            for j in range(shape[1]):
                x = i - center[0]
                y = j - center[1]
                measure = (x*x + y*y)
                r = math.sqrt(measure)
                if r < 300:
                    pxArray[i, j, 0] = 200
                    pxArray[i, j, 1] = 100
                    pxArray[i, j, 2] = 10
                else:
                    pxArray[i, j, 0] = 10
                    pxArray[i, j, 1] = 10
                    pxArray[i, j, 2] = 10

        del pxArray

    def run(self):
        returnCode = 0

        for event in pygame.event.get():
            if event.type == QUIT:
                returnCode = QUIT
                break



        self.screen.blit(self.surf, pygame.Rect(0, 0, 1200, 800))
        

        return returnCode