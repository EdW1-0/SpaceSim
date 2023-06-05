import pygame

from views.sidePanels.sideStatusPanel import SideStatusPanel

from pygame_gui.elements import UIButton, UIImage, UILabel, UITextBox, UISelectionList

class ColonyTabPanel(SideStatusPanel):
    def __init__(self, rect, manager=None):
        super().__init__(rect, manager)
        self.target_button = UIButton(pygame.Rect(0, 0, 100, 100), 
                                          text="Construction",  
                                          container = self.container, 
                                          manager=manager)
        
        self.production_button = UIButton(pygame.Rect(100, 0, 100, 100), 
                                          text="Production",  
                                          container = self.container, 
                                          manager=manager)
        
        self.vehicles_button = UIButton(pygame.Rect(200, 0, 100, 100), 
                                          text="Vehicles",  
                                          container = self.container, 
                                          manager=manager)

        self.ships_button = UIButton(pygame.Rect(300, 0, 100, 100), 
                                          text="Ships",  
                                          container = self.container, 
                                          manager=manager)
        
    def handle_event(self, event):
        self.upperEvent = 0
        if super().handle_event(event):
            return True
        elif event.ui_element == self.vehicles_button:
            self.upperEvent = 3
            return True
        else:
            return False
        
class ColonyVehiclePanel(SideStatusPanel):
    def __init__(self, rect, manager=None, colony=None):
        super().__init__(rect, manager)
        self.colony = colony

        vehicles_text = "Vehicles"
        self.vehicles_text = UILabel(pygame.Rect(0, 50, 400, 50), text=vehicles_text, manager=manager, container=self.container)

        self.vehicle_list = UISelectionList(pygame.Rect(0, 100, 400, 500),
                                            [("foo", "bar")],
                                            manager=manager,
                                            container=self.container)
        
    def update(self):
        self.vehicle_list.set_item_list([vehicle.name for vehicle in self.colony.vehicles.values()])
        self.vehicle_list.show()

class ColonyVehicleDetailPanel(SideStatusPanel):
    def __init__(self, rect, manager = None, vehicle=None):
        super().__init__(rect, manager)
        self.vehicle = vehicle

        self.vehicle_name = UILabel(pygame.Rect(200, 50, 200, 50), text = "Default name", manager=manager, container=self.container)

    def setVehicle(self, vehicle):
        self.vehicle = vehicle

    def update(self):
        if not self.vehicle:
            return
        
        self.vehicle_name.set_text(self.vehicle.name)