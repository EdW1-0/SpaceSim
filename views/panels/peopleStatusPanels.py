import pygame

from views.panels.sideStatusPanels import SideStatusPanel

from pygame_gui.elements import UILabel, UITextBox

from views.widgets.dropDownMenuId import DropDownMenuId

from peoplesim import Person
from colonysim import Building, Colony, Ship
from planetsim import Vehicle

class CrewDetailPanel(SideStatusPanel):
    def __init__(self, rect, manager=None, model=None):
        super(CrewDetailPanel, self).__init__(rect, manager)
        self.model = model
        self.person = None
        self.manager = manager

        self.person_label = UILabel(
            pygame.Rect(0, 0, 200, 100),
            text="Person placeholder",
            manager=manager,
            container=self.container,
        )
        self.person_text = UITextBox(
            "Person text",  (0, 100, 200, 200), manager=manager, container=self.container)
        
        self.location_label = UILabel(
            pygame.Rect(200, 0, 200, 100),
            text="Location placeholder",
            manager=manager,
            container=self.container,
        )

        self.transfer_menu = DropDownMenuId(
            {"Transfer": None}, 
            "Transfer", 
            pygame.Rect(200, 100, 200, 50), 
            manager=manager, 
            container=self.container
        )

        self.item_hash = ""
        
    def setPerson(self, person: Person):
        self.person = person    

    def handle_event(self, event):
        if super(CrewDetailPanel, self).handle_event(event):
            return True
        else:
            return False
        
    def validLocations(self):
        if self.person:
            if isinstance(self.person.location, Colony):
                # Get all locations
                # This means all buildings and ships and vehices plus colony itself
                colony = self.person.location
                buildings = list(colony.buildings.values())
                ships = list(colony.ships.values())
                vehicles = list(colony.vehicles.values())
                locations = {b.name: b for b in buildings} | {s.name: s for s in ships} | {v.name: v for v in vehicles} | {self.person.location.name: self.person.location}
                return locations
            elif isinstance(self.person.location.locale, Colony):
                colony = self.person.location.locale
                buildings = list(colony.buildings.values())
                ships = list(colony.ships.values())
                vehicles = list(colony.vehicles.values())
                locations = {b.name: b for b in buildings} | {s.name: s for s in ships} | {v.name: v for v in vehicles} | {self.person.location.locale.name: self.person.location.locale}
                return locations
            else:
                return {}

    def update(self):
        if self.person:
            self.person_label.set_text(self.person.name)
            self.person_text.set_text("Age: {0}<br>Sex: {1}".format(self.person.age, self.person.sex))
            if isinstance(self.person.location, Building):
                self.location_label.set_text(self.person.location.buildingClass.name)
            else:
                self.location_label.set_text(self.person.location.name)

            if isinstance(self.person.location, Colony) or isinstance(self.person.location.locale, Colony):
                # Get all locations
                # This means all buildings and ships and vehices plus colony itself
                locations = self.validLocations()
                newHash = "".join(locations.keys())
                if newHash != self.item_hash:
                    self.transfer_menu = DropDownMenuId(
                        locations, 
                        self.person.location.name, 
                        pygame.Rect(200, 100, 200, 50), 
                        manager=self.manager, 
                        container=self.container
                    )
                    self.item_hash = newHash
        
