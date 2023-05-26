from views.guiContext import GUIContext

from colonysim.colony import Colony

import pygame
from pygame_gui.elements import UILabel

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

class ColonyContext(GUIContext):
    def __init__(self, screen, model, manager, colony):
        super().__init__(screen, model, manager)
        self.colony = colony

        self.colony_name_label = UILabel(pygame.Rect(400,200,100, 100), 
                                         text="Colony name placeholder", 
                                         manager=manager)

    def run(self):
        returnCode = 0

        for event in pygame.event.get():
            if event.type == QUIT:
                returnCode = QUIT
                break

        self.colony_name_label.set_text(self.colony.name)

        self.screen.fill((250, 100, 50))

        return returnCode
