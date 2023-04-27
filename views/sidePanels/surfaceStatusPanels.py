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
        pygame.draw.rect(region_image, terrain.colour,(25,25,25,25))
        self.region_image.set_image(region_image)
        
        self.region_text.set_text("Terrain: {0}<br>Traversibility: not implemented <br>Insolation: not implemented <br>Radiation: not implemented<br>".format(terrain.name))
        

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

        self.stopButton = UIButton(pygame.Rect(0, 300, 200, 100), 
                                          text="Stop",  
                                          container = self.container, 
                                          manager=manager)

        self.targetButton = UIButton(pygame.Rect(200, 300, 200, 100), 
                                          text="Set Target",  
                                          container = self.container, 
                                          manager=manager)

    def set_vehicle(self, vehicle):
        self.vehicle = vehicle

    def handle_event(self, event):
        self.upperAction = 0
        if super(VehicleStatusPanel, self).handle_event(event):
            return True

    def update(self):
        self.vehicle_name_label.set_text(self.vehicle.name)

        self.vehicle_text.set_text("""
        Type: not implemented
        Location: {1}
        Crew: not implemented
        Fuel: {2}
        Top speed: {3}
        Range: {4}
        """.format(self.vehicle.name, self.vehicle.point, self.vehicle.fuel, self.vehicle.maxV, self.vehicle.fuelPerM))

