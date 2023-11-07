import pygame

from pygame_gui.elements import UIButton, UIImage
from pygame_gui.core import UIContainer


class SideStatusPanel:
    def __init__(self, rect, manager=None):
        self.rect = rect
        self.container = UIContainer(rect, manager=manager)
        background = pygame.Surface((rect.width, rect.height))
        pygame.draw.rect(background, (10, 10, 10), (0, 0, rect.width, rect.height))
        self.background = UIImage(
            (0, 0, rect.width, rect.height),
            background,
            manager=manager,
            container=self.container,
        )

        self.hide_button = UIButton(
            relative_rect=pygame.Rect((0, 0), (20, 20)),
            text="X",
            container=self.container,
            manager=manager,
        )

    def hide(self):
        self.container.hide()

    def show(self):
        self.container.show()

    def handle_event(self, event):
        if event.ui_element == self.hide_button:
            print("Boop!")
            self.hide()
            return True
        else:
            return False
