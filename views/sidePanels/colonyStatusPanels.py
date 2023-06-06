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
        elif event.ui_element == self.ships_button:
            self.upperEvent = 4
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

        self.vehicle_characteristics = UITextBox("Characteristics",
                                                 pygame.Rect(0, 100, 200, 100),
                                                  manager=manager,
                                                   container=self.container)
        self.vehicle_status = UITextBox("Status",
                                                 pygame.Rect(200, 100, 200, 100),
                                                  manager=manager,
                                                   container=self.container)
        self.vehicle_mission = UITextBox("Mission",
                                                 pygame.Rect(400, 100, 200, 100),
                                                  manager=manager,
                                                   container=self.container)
        self.target_button = UIButton(pygame.Rect(600, 100, 100, 50), 
                                      "Set Target",
                                        manager=manager,
                                                   container=self.container)
        self.embark_button = UIButton(pygame.Rect(600, 150, 100, 50), 
                                      "Embark",
                                        manager=manager,
                                                   container=self.container)

    def setVehicle(self, vehicle):
        self.vehicle = vehicle

    def update(self):
        if not self.vehicle:
            return
        
        self.vehicle_name.set_text(self.vehicle.name)

        self.vehicle_characteristics.set_text("Class: {0}<br>Velocity: {1}<br>Fuel per m: {2}".format(self.vehicle.vehicleClass.name, 
                                                                                             self.vehicle.maxV(),
                                                                                             self.vehicle.fuelPerM()))
        self.vehicle_status.set_text("Fuel: {0}/{1}<br>".format(self.vehicle.fuel, self.vehicle.vehicleClass.maxFuel))
        self.vehicle_mission.set_text("Orders: Not implemented<br>")

    def handle_event(self, event):
        upperAction = 0
        if super().handle_event(event):
            return True
        elif event.ui_element == self.embark_button:
            upperAction = 1
            self.hide()
            return True
        else:
            return False
        
class ColonyShipPanel(SideStatusPanel):
    def __init__(self, rect, manager=None, colony=None):
        super().__init__(rect, manager)
        self.colony = colony

        ships_text = "Ships"
        self.ships_text = UILabel(pygame.Rect(0, 50, 400, 50), text=ships_text, manager=manager, container=self.container)

        self.ships_list = UISelectionList(pygame.Rect(0, 100, 400, 500),
                                            [("foo", "bar")],
                                            manager=manager,
                                            container=self.container)
        
    def update(self):
        self.ships_list.set_item_list([ship.name for ship in self.colony.ships.values()])
        self.ships_list.show()

###TODO: Currently ColonyVehicleDetailPanel and ColonyShipDetailPanel are almost identical. Probably should merge into common superclass
class ColonyShipDetailPanel(SideStatusPanel):
    def __init__(self, rect, manager = None, ship=None):
        super().__init__(rect, manager)
        self.ship = ship

        self.ship_name = UILabel(pygame.Rect(200, 50, 200, 50), text = "Default name", manager=manager, container=self.container)

        self.ship_characteristics = UITextBox("Characteristics",
                                                 pygame.Rect(0, 100, 200, 100),
                                                  manager=manager,
                                                   container=self.container)
        self.ship_status = UITextBox("Status",
                                                 pygame.Rect(200, 100, 200, 100),
                                                  manager=manager,
                                                   container=self.container)
        self.ship_mission = UITextBox("Mission",
                                                 pygame.Rect(400, 100, 200, 100),
                                                  manager=manager,
                                                   container=self.container)
        self.target_button = UIButton(pygame.Rect(600, 100, 100, 50), 
                                      "Set Target",
                                        manager=manager,
                                                   container=self.container)
        self.launch_button = UIButton(pygame.Rect(600, 150, 100, 50), 
                                      "Launch",
                                        manager=manager,
                                                   container=self.container)
        
    def setShip(self, ship):
        self.ship = ship

    def update(self):
        if not self.ship:
            return
        
        self.ship_name.set_text(self.ship.name)

        self.ship_characteristics.set_text("Class: {0}<br>".format(self.ship.shipClass.name))
        self.ship_status.set_text("DeltaV: {0}/{1}<br>".format(self.ship.deltaV(), self.ship.shipClass.maxDeltaV))
        self.ship_mission.set_text("Orders: Not implemented<br>")

