import pygame

from views.sidePanels.sideStatusPanel import SideStatusPanel

from pygame_gui.elements import UIButton, UIImage, UILabel, UITextBox, UISelectionList
from pygame_gui.core import UIContainer

class RegionStatusPanel(SideStatusPanel):
    def __init__(self, rect, planet, manager=None, model = None):
        super(RegionStatusPanel, self).__init__(rect, manager)
        
        self.model = model
        self.planet = planet
        self.region_name_label = UILabel(pygame.Rect(0,0,rect.width, 100), 
                                         text="Region placeholder", 
                                         manager=manager, 
                                         container=self.container)
        
        region_image = pygame.Surface((50, 50))
        pygame.draw.rect(region_image, (200,200,10),(25,25,25,25))
        self.region_image = UIImage(pygame.Rect(50, 100, 50, 50), region_image, manager=manager, container=self.container)

        region_text = "Placeholder stuff"
        self.region_text = UITextBox(region_text, (0, 200, 400, 200), manager=manager, container=self.container)


    def set_region(self, region):
        self.region = region

    def update(self):
        self.region_name_label.set_text(self.region.name)

        terrain = self.model.planetSim.planetClassById(self.planet.surface.planetClass)[self.region.terrain]
        colour = terrain.colour

        region_image = pygame.Surface((50, 50))
        pygame.draw.rect(region_image, colour,(25,25,25,25))
        self.region_image.set_image(region_image)
        



        self.region_text.set_text("""Terrain: {0}
        Traversibility: not implemented
        Insolation: not implemented
        Radiation: not implemented""".format(terrain.name))
        

class VehicleStatusPanel(SideStatusPanel):
    def __init__(self, rect, manager=None, model = None):
        super(VehicleStatusPanel, self).__init__(rect, manager)
        self.model = model
        


        self.vehicle_name_label = UILabel(pygame.Rect(0,0,rect.width, 100), 
                                         text="Vehicle placeholder", 
                                         manager=manager, 
                                         container=self.container)
        
        vehicle_image = pygame.Surface((50, 50))
        pygame.draw.circle(vehicle_image, (200,200,10),(25,25),25.0)
        self.vehicle_image = UIImage(pygame.Rect(50, 100, 50, 50), vehicle_image, manager=manager, container=self.container)

        vehicle_text = "Placeholder stuff"
        self.vehicle_text = UITextBox(vehicle_text, (0, 200, 400, 200), manager=manager, container=self.container)

        self.stopButton = UIButton(pygame.Rect(0, 400, 200, 100), 
                                          text="Stop",  
                                          container = self.container, 
                                          manager=manager)
        
        self.target_button = UIButton(pygame.Rect(200, 400, 200, 100), 
                                          text="Set Target",  
                                          container = self.container, 
                                          manager=manager)

        self.upperAction = 0

    def set_vehicle(self, vehicle):
        self.vehicle = vehicle

    def handle_event(self, event):
        self.upperAction = 0
        if super(VehicleStatusPanel, self).handle_event(event):
            return True
        elif event.ui_element == self.stopButton:
            self.upperAction = 1
            return True
        elif event.ui_element == self.target_button:
            self.upperAction = 2
            return True
        else:
            return False

    def update(self):
        self.vehicle_name_label.set_text(self.vehicle.name)

        destination_text = "<None>"
        if self.vehicle.destination:
            destination_text = str(self.vehicle.destination)

        self.vehicle_text.set_text("""
        Type: not implemented
        Location: {1}
        Crew: not implemented
        Fuel: {2}
        Top speed: {3}
        Range: {4}
        Destination: {5}
        """.format(self.vehicle.name, self.vehicle.point, self.vehicle.fuel, self.vehicle.maxV, self.vehicle.fuelPerM, destination_text))

class VehicleRoutingPanel(SideStatusPanel):
    def __init__(self, rect, manager=None, model = None):
        super(VehicleRoutingPanel, self).__init__(rect, manager)
        self.model = model
        self.vehicle = None
        self.target = None

        self.source_label = UILabel(pygame.Rect(0,0,200, 100), 
                                         text="Source placeholder", 
                                         manager=manager, 
                                         container=self.container)
        self.target_label = UILabel(pygame.Rect(200,0,200, 100), 
                                         text="Target placeholder", 
                                         manager=manager, 
                                         container=self.container)
        self.route_text = UITextBox("Route text", 
                                    pygame.Rect(0, 100, 200, 100), 
                                    manager=manager, 
                                    container=self.container)
        self.confirm_button = UIButton(pygame.Rect(200, 100, 200, 100), 
                                       text = "Confirm", 
                                       manager = manager, 
                                       container = self.container)

    def set_vehicle(self, vehicle):
        self.vehicle = vehicle

    def set_target(self, target):
        self.target = target
        self.update()

    def update(self):
        if self.vehicle:
            self.source_label.set_text(str(self.vehicle.point))
        else:
            self.source_label.set_text("")
        
        if self.target:
            self.target_label.set_text(str(self.target))
        else:
            self.target_label.set_text("")

    def handle_event(self, event):
        self.upperAction = 0
        if super(VehicleRoutingPanel, self).handle_event(event):
            return True
        elif event.ui_element == self.confirm_button:
            self.vehicle.setDestination(self.target)
            self.hide()
            self.upperAction = 1
            return True
        else:
            return False
