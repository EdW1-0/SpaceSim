from views.guiContext import GUIContext

import pygame

from pygame.locals import (
    QUIT,
)

class TechContext(GUIContext):
    def run(self):
        returnCode = 0

        for event in pygame.event.get():
            if event.type == QUIT:
                returnCode = QUIT
                break
                        
            self.manager.process_events(event)


        self.screen.fill((140, 0, 25))

        return returnCode
