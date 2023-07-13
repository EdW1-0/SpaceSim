import pygame

from views.sidePanels.sideStatusPanel import SideStatusPanel

from pygame_gui.elements import UIButton, UIImage, UILabel, UITextBox, UISelectionList

from orbitsim.orbitTrajectory import TrajectoryState

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
        

###TODO: Currently ColonyVehicleDetailPanel and ColonyShipDetailPanel are almost identical. Probably should merge into common superclass
class ColonyShipDetailPanel(SideStatusPanel):
    def __init__(self, rect, manager = None, orbitSim = None, ship=None):
        super().__init__(rect, manager)
        self.ship = ship
        self.orbitSim = orbitSim

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
        self.launch_button.hide()
        
    def setShip(self, ship):
        self.ship = ship 

    def update(self):
        if not self.ship:
            self.hide()
            return
        
        self.ship_name.set_text(self.ship.name)

        self.ship_characteristics.set_text("Class: {0}<br>".format(self.ship.shipClass.name))
        self.ship_status.set_text("DeltaV: {0}/{1}<br>".format(self.ship.deltaV(), self.ship.shipClass.maxDeltaV))


        trajectory = self.trajectory()
        if trajectory:
            self.ship_mission.set_text(trajectory.strRep(self.orbitSim))
            self.launch_button.show()
        else:               
            self.ship_mission.set_text("Orders: Not implemented<br>")
            self.launch_button.hide()
        

    def trajectory(self):
        if not self.ship:
            return None

        particle = None
        for p in self.orbitSim._particles.values():
            if p.payload == self.ship:
                particle = p

        traj = False
        trajectory = None
        if particle:
            try:
                trajectory = self.orbitSim.trajectoryForParticle(particle.id)
                traj = True
            except KeyError:
                pass
        
        return trajectory

    def handle_event(self, event):
        self.upperAction = 0
        if super(ColonyShipDetailPanel, self).handle_event(event):
            return True
        elif event.ui_element == self.target_button:
            self.upperAction = 1
            return True
        elif event.ui_element == self.launch_button:
            self.upperAction = 2
            return True
        else:
            return False


class ColonyItemPanel(SideStatusPanel):
    def __init__(self, rect, manager=None, colony=None, title = "Default title", sourceList = None):
        super().__init__(rect, manager)
        self.colony = colony
        self.sourceList = sourceList
        self.item_hash = ""

        self.title_text = UILabel(pygame.Rect(0, 50, 400, 50), text=title, manager=manager, container=self.container)

        self.item_list = UISelectionList(pygame.Rect(0, 100, 400, 500),
                                            [],
                                            manager=manager,
                                            container=self.container)
    def update(self):
        newHash = "".join(map(str, [item.id for item in self.sourceList.values()]))
        if newHash != self.item_hash:
            self.item_list.set_item_list([item.name for item in self.sourceList.values()])
            self.item_list.show()
            self.item_hash = newHash