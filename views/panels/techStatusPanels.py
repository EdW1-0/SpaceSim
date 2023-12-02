import pygame

from pygame_gui.elements import (
    UIButton, 
    UIImage, 
    UILabel, 
    UITextBox, 
    UISelectionList,
)
from pygame_gui import UIManager

from views.panels.sideStatusPanels import SideStatusPanel

from gameModel import GameModel
from techtree import (
    TechNode,
    TechTree
)


class TechStatusPanel(SideStatusPanel):
    def __init__(self, rect: pygame.Rect, manager: UIManager=None, model: GameModel=None) -> None:
        super(TechStatusPanel, self).__init__(rect, manager)

        self.tech_label = UILabel(pygame.Rect(100, 100, 200, 100), "<Tech name placeholder>", manager=manager, container=self.container)
        self.tech: TechNode = None


    def update(self):
        if self.tech:
            self.tech_label.set_text(self.tech.name)

