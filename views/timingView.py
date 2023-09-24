import pygame

from pygame_gui.elements import (
    UIButton,
    UIImage,
    UILabel
)

from pygame_gui.core import UIContainer


class TimingPanel:
    def __init__(self, rect, manager=None, timingMaster=None):
        self.rect = rect
        self.timingMaster = timingMaster
        self.container = UIContainer(rect, manager=manager)
        background = pygame.Surface((rect.width, rect.height))
        pygame.draw.rect(background,
                         (10, 10, 10),
                         (0, 0, rect.width, rect.height))

        self.background = UIImage((0, 0, rect.width, rect.height),
                                  background,
                                  manager=manager,
                                  container=self.container)

        start_text = ">"
        self.start_button = UIButton(pygame.Rect(10, 10, 40, 80),
                                     text=start_text,
                                     container=self.container,
                                     manager=manager)

        step_text = ">|"
        self.step_button = UIButton(pygame.Rect(60, 10, 40, 80),
                                    text=step_text,
                                    container=self.container,
                                    manager=manager)

        stop_text = "[]"
        self.stop_button = UIButton(pygame.Rect(110, 10, 40, 80),
                                    text=stop_text,
                                    container=self.container,
                                    manager=manager)

        time_text = "-1"
        self.time_label = UILabel(pygame.Rect(210, 10, 180, 80),
                                  text=time_text,
                                  manager=manager,
                                  container=self.container)

    def handle_event(self, event):
        print(self.timingMaster.timestamp)
        if event.ui_element == self.start_button:
            self.timingMaster.start()
        elif event.ui_element == self.step_button:
            self.timingMaster.step()
        elif event.ui_element == self.stop_button:
            self.timingMaster.stop()

    def update(self):
        self.time_label.set_text(str(self.timingMaster.timestamp))
