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
    TechTree,
    PlayerTech
)


class TechStatusPanel(SideStatusPanel):
    def __init__(self, rect: pygame.Rect, manager: UIManager=None, model: GameModel=None) -> None:
        super(TechStatusPanel, self).__init__(rect, manager)

        self.name_label = UILabel(pygame.Rect(100, 0, 200, 50), 
                                  "<Tech name placeholder>", 
                                  manager=manager, 
                                  container=self.container)
        self.tech: TechNode = None

        self.model = model

        self.cost_label = UILabel(pygame.Rect(100, 50, 200, 50), 
                                  "<Tech cost placeholder>", 
                                  manager=manager, 
                                  container=self.container)
        self.description_text = UITextBox("<Tech description placeholder", 
                                          (0, 100, 400, 200), 
                                          manager=manager, 
                                          container=self.container)
        
        self.effects_label = UILabel(pygame.Rect(100, 300, 200, 50), 
                                  "Effects", 
                                  manager=manager, 
                                  container=self.container)
        self.effects_list = UISelectionList(pygame.Rect(0, 350, 400, 100),
            [("foo", "bar")],
            manager=manager,
            container=self.container,)
        self.requires_label = UILabel(pygame.Rect(0, 450, 200, 50), 
                                  "Requires", 
                                  manager=manager, 
                                  container=self.container)
        self.requires_list = UISelectionList(pygame.Rect(0, 500, 200, 100),
            [("foo", "bar")],
            manager=manager,
            container=self.container,)
        self.unlocks_label = UILabel(pygame.Rect(200, 450, 200, 50), 
                                  "Unlocks", 
                                  manager=manager, 
                                  container=self.container)
        self.unlocks_list = UISelectionList(pygame.Rect(200, 500, 200, 100),
            [("foo", "bar")],
            manager=manager,
            container=self.container,)
        
        self.research_button = UIButton(pygame.Rect(0, 600, 400, 100),
                                        text="Research",
                                        manager=manager,
                                        container=self.container,)
        
        


    def update(self):
        self.research_button.hide()

        if self.tech:
            self.name_label.set_text(self.tech.name)
            self.cost_label.set_text(str(self.tech.cost))
            self.description_text.set_text(str(self.tech.description))

            self.effects_list.set_item_list([e.__str__() for e in self.tech.effects])

            self.requires_list.set_item_list([self.model.techTree.nodeById(a).name for a in self.tech.ancestors])
            self.unlocks_list.set_item_list([tech.name for tech in self.model.techTree.descendentsOfId(self.tech.id)])

            if self.tech.id in self.model.playerTech.possibleTargets:
                self.research_button.show()

            

class TechProgressPanel(SideStatusPanel):
    def __init__(self, rect: pygame.Rect, manager: UIManager=None, playerTech: PlayerTech=None) -> None:
        super(TechProgressPanel, self).__init__(rect, manager)
        self.playerTech = playerTech

        self.tech_label =  UILabel(pygame.Rect(0, 0, 100, 50), 
                                  "<Active tech placeholder>", 
                                  manager=manager, 
                                  container=self.container)

        self.progress_label = UILabel(pygame.Rect(100, 0, 50, 50), 
                                  "0", 
                                  manager=manager, 
                                  container=self.container)
        
        self.hide_button.hide()

    def update(self):
        if self.playerTech.activeTech:
            self.tech_label.set_text(self.playerTech.activeTech.name)
            self.progress_label.set_text(str(self.playerTech.progress) + "/" + str(self.playerTech.activeTech.cost))
        else:
            self.tech_label.set_text("None")
            self.progress_label.set_text("0")