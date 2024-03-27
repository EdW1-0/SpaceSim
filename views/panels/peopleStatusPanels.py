import pygame

from views.panels.sideStatusPanels import SideStatusPanel

from pygame_gui.elements import UILabel, UITextBox

from peoplesim import Person

class CrewDetailPanel(SideStatusPanel):
    def __init__(self, rect, manager=None, model=None):
        super(CrewDetailPanel, self).__init__(rect, manager)
        self.model = model
        self.person = None

        self.person_label = UILabel(
            pygame.Rect(0, 0, 200, 100),
            text="Person placeholder",
            manager=manager,
            container=self.container,
        )
        self.person_text = UITextBox(
            "Person text",  (0, 100, 200, 200), manager=manager, container=self.container)
        
    def setPerson(self, person: Person):
        self.person = person    

    def handle_event(self, event):
        if super(CrewDetailPanel, self).handle_event(event):
            return True
        else:
            return False

    def update(self):
        if self.person:
            self.person_label.set_text(self.person.name)
            self.person_text.set_text("Age: {0}<br>Sex: {1}".format(self.person.age, self.person.sex))
        
