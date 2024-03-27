import pygame

from pygame_gui.elements import UIButton, UIImage, UILabel, UITextBox, UISelectionList

from views.panels.sideStatusPanels import SideStatusPanel

from orbitsim import OrbitNode

from planetsim import SurfacePoint, SurfaceBase



class PlanetStatusPanel(SideStatusPanel):
    def __init__(self, rect, manager=None, model=None):
        super(PlanetStatusPanel, self).__init__(rect, manager)

        self.model = model
        self.planet_name_label = UILabel(
            pygame.Rect(0, 0, rect.width, 100),
            text="Planet placeholder",
            manager=manager,
            container=self.container,
        )

        planet_image = pygame.Surface((50, 50))
        pygame.draw.circle(planet_image, (200, 200, 10), (25, 25), 25)
        self.planet_image = UIImage(
            pygame.Rect(50, 100, 50, 50),
            planet_image,
            manager=manager,
            container=self.container,
        )

        planet_text = "Placeholder stuff"
        self.planet_text = UITextBox(
            planet_text, (0, 200, 400, 200), manager=manager, container=self.container
        )

        atmosphere_text = "Atmosphere"
        self.atmosphere_button = UIButton(
            pygame.Rect(0, 400, 200, 100),
            text=atmosphere_text,
            container=self.container,
            manager=manager,
        )

        surface_text = "Surface"
        self.surface_button = UIButton(
            pygame.Rect(200, 400, 200, 100),
            text=surface_text,
            container=self.container,
            manager=manager,
        )

        self.station_list = UISelectionList(
            pygame.Rect(0, 500, 400, 100),
            [("foo", "bar")],
            manager=manager,
            container=self.container,
        )

        self.node = None
        self.planet = None

    def set_node(self, node):
        self.node = node

    def set_planet(self, planet):
        self.planet = planet

    def update(self):
        if self.node:
            self.planet_name_label.set_text(self.node.name)
            self.station_list.set_item_list(
                [
                    self.model.orbitSim.particleById(id).payload.name
                    for id in self.node.particles
                ]
            )
            self.station_list.show()
        else:
            self.planet_name_label.set_text(self.planet.name)
            self.surface_button.hide()
            self.station_list.hide()

        self.planet_text.set_text(
            "Gravity: {0}m/s/s<br>Mass: madeupnumber".format(self.planet.gravity)
        )

    def handle_event(self, event):
        self.upperAction = 0
        if super(PlanetStatusPanel, self).handle_event(event):
            return True
        elif event.ui_element == self.surface_button:
            self.upperAction = 1
            return True
        else:
            return False


class OrbitStatusPanel(SideStatusPanel):
    def __init__(self, rect, manager=None, model=None):
        super(OrbitStatusPanel, self).__init__(rect, manager)
        self.model = model
        self.orbit_name_label = UILabel(
            pygame.Rect(0, 0, rect.width, 100),
            text="Orbit placeholder",
            manager=manager,
            container=self.container,
        )

        self.station_list = UISelectionList(
            pygame.Rect(0, 500, 400, 100),
            [("foo", "bar")],
            manager=manager,
            container=self.container,
        )

    def set_node(self, node):
        self.node = node

    def update(self):
        self.orbit_name_label.set_text(self.node.name)
        self.station_list.set_item_list(
            [
                self.model.orbitSim.particleById(id).payload.name
                for id in self.node.particles
            ]
        )
        self.station_list.show()


class LinkStatusPanel(SideStatusPanel):
    def __init__(self, rect, manager=None):
        super(LinkStatusPanel, self).__init__(rect, manager)

        self.link_name_label = UILabel(
            pygame.Rect(0, 0, rect.width, 100),
            text="Link placeholder",
            manager=manager,
            container=self.container,
        )

    def set_link(self, link):
        self.link = link

    def update(self):
        self.link_name_label.set_text(
            "{0} - {1}".format(self.link.topNode, self.link.bottomNode)
        )


class ShipStatusPanel(SideStatusPanel):
    def __init__(self, rect, manager=None, model=None):
        super(ShipStatusPanel, self).__init__(rect, manager)
        self.model = model
        self.particle = None
        self.ship_name_label = UILabel(
            pygame.Rect(0, 0, rect.width, 100),
            text="Ship placeholder",
            manager=manager,
            container=self.container,
        )

        ship_text = "Placeholder text"
        self.ship_text = UITextBox(
            ship_text, (0, 100, 200, 200), manager=manager, container=self.container
        )

        self.trajectory_text = UITextBox(
            "No trajectory",
            (200, 100, 200, 200),
            manager=manager,
            container=self.container,
        )

        self.locationButton = UIButton(
            pygame.Rect(0, 300, 200, 100),
            text="Location",
            container=self.container,
            manager=manager,
        )

        self.targetButton = UIButton(
            pygame.Rect(200, 300, 200, 100),
            text="Set Target",
            container=self.container,
            manager=manager,
        )

        self.crewList = UISelectionList(
            pygame.Rect(0, 400, 400, 100),
            [("foo", "bar")],
            manager=manager,
            container=self.container,            
        )

        # This is how we end up passing control up to OrbitContext
        # to switch out a view or otherwise do something.
        # I think there must be a better way, so revise this later.
        # TODO: Improve on this mess!
        self.upperAction = 0

    def handle_event(self, event):
        self.upperAction = 0
        if super(ShipStatusPanel, self).handle_event(event):
            return True
        elif event.ui_element == self.locationButton:
            self.upperAction = 1
            return True
        elif event.ui_element == self.targetButton:
            self.upperAction = 2
            return True
        else:
            return False

    def set_particle(self, particle):
        self.particle = particle

    def ship_location(self):
        try:
            location = self.model.orbitSim._particleLocation(self.particle.id)
        except KeyError:
            location = None
        return location

    def ship_trajectory(self):
        trajectory = None
        try:
            trajectory = self.model.orbitSim.trajectoryForParticle(self.particle.id)
        except KeyError:
            trajectory = None

        return trajectory

    def update(self):
        if not self.particle:
            self.hide()
            return

        self.ship_name_label.set_text(self.particle.payload.name)

        location = self.ship_location()
        if not location:
            self.hide()
            return

        if isinstance(location, OrbitNode):
            locationText = location.name
        else:
            locationText = (
                self.model.orbitSim.nodeById(location.topNode).name
                + "/"
                + self.model.orbitSim.nodeById(location.bottomNode).name
            )

        self.ship_text.set_text(
            "Delta V: {0}m/s<br>Velocity: {1}m/s<br>Location: {2}".format(
                self.particle.deltaV(), self.particle.velocity, locationText
            )
        )

        trajectory = self.ship_trajectory()
        if trajectory:
            self.trajectory_text.set_text(trajectory.strRep(self.model.orbitSim))
        else:
            self.trajectory_text.set_text("No trajectory")

        
        self.crewList.set_item_list(
            [self.model.peopleSim.personById(id).name for id in self.particle.payload.crew]
        )


class TargetSettingPanel(SideStatusPanel):
    def __init__(self, rect, manager=None, model=None):
        super(TargetSettingPanel, self).__init__(rect, manager)
        self.model = model
        self.ship = None
        self.source = None
        self.target = None
        self.trajectory = None

        self.source_label = UILabel(
            pygame.Rect(0, 0, 200, 100),
            text="Source placeholder",
            manager=manager,
            container=self.container,
        )
        self.target_label = UILabel(
            pygame.Rect(200, 0, 200, 100),
            text="Target placeholder",
            manager=manager,
            container=self.container,
        )
        self.route_text = UITextBox(
            "Route text",
            pygame.Rect(0, 100, 200, 200),
            manager=manager,
            container=self.container,
        )
        self.confirm_button = UIButton(
            pygame.Rect(200, 200, 200, 100),
            text="Confirm",
            manager=manager,
            container=self.container,
        )
        self.surface_button = UIButton(
            pygame.Rect(200, 100, 200, 100),
            text="Surface target",
            manager=manager,
            container=self.container,
        )
        self.surface_button.hide()

    def set_ship(self, ship):
        self.ship = ship

    def set_source(self, source):
        self.source = source

    def set_target(self, target):
        self.target = target


    def set_coordinates(self, coordinates):
        assert self.trajectory
        self.trajectory.surfaceCoordinates = coordinates
        self.update()

    def clear_state(self):
        self.ship = None
        self.source = None
        self.target = None
        self.trajectory = None
        self.update()

    def update(self):
        if self.source:
            self.source_label.set_text(self.source.name)
        else:
            self.source_label.set_text("")

        if self.target:
            self.target_label.set_text(self.target.name)
            if self.target.planet:
                planet = self.model.planetSim.planetById(self.target.planet)
                if planet.surface:
                    self.surface_button.show()
                else:
                    self.surface_button.hide()
            else:
                self.surface_button.hide()
        else:
            self.target_label.set_text("")
            self.surface_button.hide()

        if self.trajectory:
            dv = self.model.orbitSim._deltaVCost(self.trajectory.trajectory)
            time = self.model.orbitSim._totalTime(self.trajectory.trajectory)
            distance = self.model.orbitSim._totalDistance(self.trajectory.trajectory)
            if self.trajectory.surfaceCoordinates and isinstance(
                self.trajectory.surfaceCoordinates, SurfacePoint
            ):
                coords = (
                    self.trajectory.surfaceCoordinates.latitude,
                    self.trajectory.surfaceCoordinates.longitude,
                )
                self.route_text.set_text(
                    "Delta V: {0}m/s<br>"
                    "Total time: {1}<br>"
                    "Total distance: {2}<br>"
                    "Coords: {3}".format(
                        dv, time, distance, coords
                    )
                )
            elif self.trajectory.surfaceCoordinates and isinstance(
                self.trajectory.surfaceCoordinates, SurfaceBase
            ):
                baseName = self.trajectory.surfaceCoordinates.name
                self.route_text.set_text(
                    "Delta V: {0}m/s<br>"
                    "Total time: {1}<br>"
                    "Total distance: {2}<br>"
                    "Rendezvous: {3}".format(
                        dv, time, distance, baseName
                    )
                )
            else:
                self.route_text.set_text(
                    "Delta V: {0}m/s<br>Total time: {1}<br>Total distance: {2}".format(
                        dv, time, distance
                    )
                )
        else:
            self.route_text.set_text("")

    def handle_event(self, event):
        if super(TargetSettingPanel, self).handle_event(event):
            return True
        elif event.ui_element == self.confirm_button:
            return True
        elif event.ui_element == self.surface_button:
            return True
        else:
            return False


