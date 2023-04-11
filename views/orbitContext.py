import pygame
import pygame_gui
from pygame_gui.elements import UIButton, UIImage, UILabel, UITextBox, UISelectionList
from pygame_gui.core import UIContainer

from views.guiContext import GUIContext
from views.timingView import TimingPanel

from orbitsim.orbitNode import LeafClass, OrbitNode
from orbitsim.orbitLink import OrbitLink

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    MOUSEBUTTONUP,
    MOUSEWHEEL,
    QUIT,
)

LOADMENUVIEW = pygame.USEREVENT + 2

class OrbitNodeView(pygame.sprite.Sprite):
    def __init__(self, node, center=(0, 0), selected = False):
        super(OrbitNodeView, self).__init__()
        self.center = center
        self.node = node
        self.surf = pygame.surface.Surface((22, 22))
        self.surf.set_colorkey((0, 0, 0))
        color = None
        if self.node.leaf == LeafClass.NONE:
            color = (50, 50, 150)
        elif self.node.leaf == LeafClass.ROOT:
            color = (250, 250, 100)
        elif self.node.leaf == LeafClass.PLANET:
            color = (150, 250, 150)
        elif self.node.leaf == LeafClass.MOON:
            color = (100, 100, 100)
        else:
            color = (200, 0, 0)
        pygame.draw.circle(self.surf, color, (11, 11), 10.0)

        if selected:
            pygame.draw.circle(self.surf, (250, 0, 0), (11,11), 11.0, width=1)

        self.rect = self.surf.get_rect(center = self.center)

        

class OrbitNodeViewLabel(pygame.sprite.Sprite):
    def __init__(self, node, center=(0, 0)):
        super(OrbitNodeViewLabel, self).__init__()
        self.node = node
        font = pygame.font.Font(size=18)
        self.surf = font.render(self.node.name, True, (230, 230, 230))
        self.rect = self.surf.get_rect()
        self.rect.center = center

class OrbitLinkViewLabel(pygame.sprite.Sprite):
    def __init__(self, link, center=(0, 0)):
        super(OrbitLinkViewLabel, self).__init__()
        self.link = link
        font = pygame.font.Font(size=18)
        self.surf = font.render(str(self.link.deltaV), True, (230, 230, 120))
        self.rect = self.surf.get_rect()
        self.rect.center = center


class OrbitLinkView(pygame.sprite.Sprite):
    def __init__(self, link, start = (0,0), end = (0,0)):
        super(OrbitLinkView, self).__init__()


        left = min(start[0], end[0])
        width = max(abs(end[0] - start[0]), 10)

        top = min(start[1], end[1])
        height = max(abs(end[1] - start[1]), 10)

        # Adjust rect a bit to account for the margins needed for nodes, and to offset start to midpoint of rect
        if height > width:
            left = left - 5
            top = top + 10
            height = height - 20
        else:
            top = top - 5
            left = left + 10
            width = width - 20
        
        # May have shrunk to zero if zoomed, that's OK, but don't let it go below zero or we crash
        width = max(width, 0)
        height = max(height, 0)
        self.start = start
        self.end = end
        self.link = link
        self.surf = pygame.surface.Surface((width, height))
        self.surf.set_colorkey((0, 0, 0))
        pygame.draw.rect(self.surf, (50, 200, 50), (0, 0, width, height))
        self.rect = self.surf.get_rect(top = top, left=left)

class ParticleView(pygame.sprite.Sprite):
    def __init__(self, particle, center = (0, 0)):
        super(ParticleView, self).__init__()
        self.particle = particle
        self.surf = pygame.surface.Surface((10, 10))
        self.surf.set_colorkey((0, 0, 0))
        pygame.draw.rect(self.surf, (200, 50, 50), (0, 0, 10, 10))
        self.rect = self.surf.get_rect(center=center)


class SideStatusPanel:
    def __init__(self, rect, manager=None):
        self.rect = rect
        self.container = UIContainer(rect, manager = manager)
        background = pygame.Surface((rect.width,rect.height))
        pygame.draw.rect(background, (10, 10, 10), (0, 0, rect.width, rect.height))
        self.background = UIImage((0,0,rect.width,rect.height), background, manager = manager, container=self.container)

        self.hide_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0,0), (20, 20)), 
                                                        text='X', 
                                                        container=self.container, 
                                                        manager=manager)
        
    def hide(self):
        self.container.hide()

    def show(self):
        self.container.show()

    def handle_event(self, event):
        if event.ui_element == self.hide_button:
            print("Boop!") 
            self.hide()
            return True
        else:
            return False


class PlanetStatusPanel(SideStatusPanel):
    def __init__(self, rect, manager=None, model=None):
        super(PlanetStatusPanel, self).__init__(rect, manager)
        
        self.model = model
        self.planet_name_label = UILabel(pygame.Rect(0,0,rect.width, 100), 
                                         text="Planet placeholder", 
                                         manager=manager, 
                                         container=self.container)
        
        planet_image = pygame.Surface((50, 50))
        pygame.draw.circle(planet_image, (200,200,10),(25,25), 25)
        self.planet_image = UIImage(pygame.Rect(50, 100, 50, 50), planet_image, manager=manager, container=self.container)

        planet_text = "Placeholder stuff"
        self.planet_text = UITextBox(planet_text, (0, 200, 400, 200), manager=manager, container=self.container)

        atmosphere_text = "Atmosphere"
        self.atmosphere_button = UIButton(pygame.Rect(0, 400, 200, 100), 
                                          text=atmosphere_text, 
                                          container = self.container, 
                                          manager=manager)

        surface_text = "Surface"
        self.surface_button = UIButton(pygame.Rect(200, 400, 200, 100), 
                                          text=surface_text, 
                                          container = self.container, 
                                          manager=manager)

        self.station_list = UISelectionList(pygame.Rect(0, 500, 400, 100),
                                            [("foo", "bar")],
                                            manager=manager,
                                            container=self.container)
     
    def set_node(self, node):
        self.node = node

    def set_planet(self, planet):
        self.planet = planet

    def update(self):
        self.planet_name_label.set_text(self.node.name)
        self.planet_text.set_text("Gravity: {0}m/s/s<br>Mass: madeupnumber".format(self.planet.gravity))
        self.station_list.set_item_list([self.model.orbitSim.particleById(id).payload.name for id in self.node.particles])

class OrbitStatusPanel(SideStatusPanel):
    def __init__(self, rect, manager=None):
        super(OrbitStatusPanel, self).__init__(rect, manager)

        self.orbit_name_label = UILabel(pygame.Rect(0,0,rect.width, 100), 
                                         text="Orbit placeholder", 
                                         manager=manager, 
                                         container=self.container)

    def set_node(self, node):
        self.node = node 

    def update(self):
        self.orbit_name_label.set_text(self.node.name)

class LinkStatusPanel(SideStatusPanel):
    def __init__(self, rect, manager=None):
        super(LinkStatusPanel, self).__init__(rect, manager)

        self.link_name_label = UILabel(pygame.Rect(0,0,rect.width, 100), 
                                         text="Link placeholder", 
                                         manager=manager, 
                                         container=self.container)
        
    def set_link(self, link):
        self.link = link

    def update(self):
        self.link_name_label.set_text("{0} - {1}".format(self.link.topNode, self.link.bottomNode))
        

class ShipStatusPanel(SideStatusPanel):
    def __init__(self, rect, manager=None, model = None):
        super(ShipStatusPanel, self).__init__(rect, manager)
        self.model = model
        self.ship = None
        self.ship_name_label = UILabel(pygame.Rect(0, 0, rect.width, 100),
                                       text = "Ship placeholder",
                                       manager = manager,
                                       container = self.container)
        
        ship_text = "Placeholder text"
        self.ship_text = UITextBox(ship_text, (0, 100, 200, 200), manager=manager, container=self.container)

        self.trajectory_text = UITextBox("No trajectory", (200, 100, 200, 200), manager=manager, container=self.container)

        self.locationButton = UIButton(pygame.Rect(0, 300, 200, 100), 
                                          text="Location",  
                                          container = self.container, 
                                          manager=manager)

        self.targetButton = UIButton(pygame.Rect(200, 300, 200, 100), 
                                          text="Set Target",  
                                          container = self.container, 
                                          manager=manager)
        
        # This is how we end up passing control up to OrbitContext to switch out a view or otherwise do something.
        # I think there must be a better way, so revise this later.
        ###TODO: Improve on this mess!
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

        
    def set_ship(self, ship):
        self.ship = ship

    def ship_location(self):
        return self.model.orbitSim._particleLocation(self.ship.id)
    
    def ship_trajectory(self):
        trajectory = None
        try:
            trajectory = self.model.orbitSim.trajectoryForParticle(self.ship.id)
        except KeyError:
            trajectory = None

        return trajectory

    def update(self):
        if not self.ship:
            return
        
        self.ship_name_label.set_text(self.ship.payload.name)

        location = self.ship_location()

        if isinstance(location, OrbitNode):
            locationText = location.name 
        else:
            locationText = self.model.orbitSim.nodeById(location.topNode).name + "/" + self.model.orbitSim.nodeById(location.bottomNode).name


        self.ship_text.set_text("Delta V: {0}m/s<br>Velocity: {1}m/s<br>Location: {2}".format(self.ship.deltaV(), 
                                                                                              self.ship.velocity, 
                                                                                              locationText))
        
        
        trajectory = self.ship_trajectory()
        if trajectory:
            trajectoryText = ""
            for node in trajectory.allNodes():
                orbitNode = self.model.orbitSim.nodeById(node)
                trajectoryText += (orbitNode.name + "<br>")

            self.trajectory_text.set_text(trajectoryText)
        
        else:
            self.trajectory_text.set_text("No trajectory")

class TargetSettingPanel(SideStatusPanel):
    def __init__(self, rect, manager=None, model = None):
        super(TargetSettingPanel, self).__init__(rect, manager)
        self.model = model
        self.ship = None
        self.source = None
        self.target = None
        self.trajectory = None

        self.source_label = UILabel(pygame.Rect(0,0,200, 100), 
                                         text="Source placeholder", 
                                         manager=manager, 
                                         container=self.container)
        self.target_label = UILabel(pygame.Rect(200,0,200, 100), 
                                         text="Target placeholder", 
                                         manager=manager, 
                                         container=self.container)
        self.route_text = UITextBox("Route text", 
                                    pygame.Rect(0, 100, 200, 200), 
                                    manager=manager, 
                                    container=self.container)
        self.confirm_button = UIButton(pygame.Rect(200, 100, 200, 200), 
                                       text = "Confirm", 
                                       manager = manager, 
                                       container = self.container)

    def set_ship(self, ship):
        self.ship = ship

    def set_source(self, source):
        self.source = source

    def set_target(self, target):
        self.target = target
        if self.trajectory:
            self.model.orbitSim.cancelTrajectory(self.ship.id)
        self.trajectory = self.model.orbitSim.createTrajectory(self.target.id, self.ship.id, self.source.id)
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
        else:
            self.target_label.set_text("")

        if self.trajectory:
            dv = self.model.orbitSim._deltaVCost(self.trajectory.trajectory)
            time = self.model.orbitSim._totalTime(self.trajectory.trajectory)
            distance = self.model.orbitSim._totalDistance(self.trajectory.trajectory)
            self.route_text.set_text("Delta V: {0}m/s<br>Total time: {1}<br>Total distance: {2}".format(dv, time, distance))
        else:
            self.route_text.set_text("")






class OrbitContext(GUIContext):
    def __init__(self, screen, model, manager, boundsRect = pygame.Rect(-100, -100, 1400, 2000)):
        super(OrbitContext, self).__init__(screen, model, manager)
        self.all_sprites = pygame.sprite.Group()
        self.node_sprites = pygame.sprite.Group()
        self.link_sprites = pygame.sprite.Group()
        self.particle_sprites = pygame.sprite.Group()

        self.selected_node = None

        self.boundsRect = boundsRect
        self.scale = 1.0
        self.basePoint = (400, 750)

        self.computeLayout()

        self.hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 0), (100, 50)),
                                             text='Settings',
                                             manager=manager)

        summary_rect = pygame.Rect(800, 200, 400, 600)
        timing_rect = pygame.Rect(800, 0, 400, 200)
        target_rect = pygame.Rect(400, 600, 400, 200)
        
        self.planet_summary = PlanetStatusPanel(summary_rect, manager=manager, model = self.model)
        #self.planet_window.add_element(self.boop_button)
        self.planet_summary.hide()

        self.orbit_summary = OrbitStatusPanel(summary_rect, manager=manager)
        self.orbit_summary.hide()

        self.link_summary = LinkStatusPanel(summary_rect, manager=manager)
        self.link_summary.hide()

        self.ship_summary = ShipStatusPanel(summary_rect, manager=manager, model = self.model)
        self.ship_summary.hide()

        self.active_summary = None

        self.target_panel = TargetSettingPanel(target_rect, manager=manager, model = self.model)
        self.target_panel.hide()

        self.timing_panel = TimingPanel(timing_rect, manager=manager, timingMaster=self.model.timingMaster)

        self.target_mode = False

    def computeLayout(self):
        self.all_sprites.empty()
        self.node_sprites.empty()
        self.link_sprites.empty()
        self.particle_sprites.empty()

        # First label root node. By convention node 0 (surface of sun)
        rootNode = self.model.orbitSim.nodeById("SUS")
        terminalNode = self.model.orbitSim.nodeById("SSE")
        sunSpot = self.basePoint

        trunkPath = self.model.orbitSim._findPath(rootNode.id, terminalNode.id, [])[0]
        # Draw trunk - path is node/link/node/link/node so just skip links for now
        self.drawPath(trunkPath, start = sunSpot, yStep = -140)


        # Then find all planet leaf nodes
        planetNodes = []
        for node in self.model.orbitSim._nodes.values():
            if (node.leaf == LeafClass.PLANET and node.id != 0):
                planetNodes.append(node)

        # Then find all paths from root to leaves
        planetPaths = [self.model.orbitSim._findPath(rootNode.id, node.id, [])[0] for node in planetNodes]
        branchPaths = [self.branchPath(path, trunkPath) for path in planetPaths]

        # Now draw the branch.
        count = 0
        for path in branchPaths:
            # Start by finding the view for the branch point, so we know what height to draw from
            branchPoint = path[0]
            branchRoot = (0,0)
            for ov in self.node_sprites:
                if ov.node.id == branchPoint:
                    branchRoot = ov.center

            # Alternate the direction of drawing
            reverse = 2*(count % 2) - 1
            count += 1

            self.drawPath(path, start = branchRoot, xStep = reverse*120, skip = branchPoint)

        
        # Now handle moons
        moonNodes = []
        for node in self.model.orbitSim._nodes.values():
            if (node.leaf == LeafClass.MOON and node.id != 0):
                moonNodes.append(node)

        moonPaths = [self.model.orbitSim._findPath(rootNode.id, node.id, [])[0] for node in moonNodes]
        moonFromTrunkPaths = [self.branchPath(path, trunkPath) for path in moonPaths]

        for moonPath in moonFromTrunkPaths:
            # Now find the right branch
            moonSubPath = None
            for branch in branchPaths:
                if branch[0] != moonPath[0]:
                    continue

                moonSubPath = self.branchPath(moonPath, branch)

            moonSpot = (0,0)
            moonRoot = moonSubPath[0]
            for ov in self.node_sprites:
                if ov.node.id == moonRoot:
                    moonSpot = ov.center

            self.drawPath(moonSubPath, start = moonSpot, yStep = 60, skip = moonRoot)

        for view in self.node_sprites:
            ov = OrbitNodeViewLabel(view.node, (view.center[0], view.center[1]+15))
            self.all_sprites.add(ov)

        for view in self.link_sprites:
            ov = OrbitLinkViewLabel(view.link, view.rect.center)
            self.all_sprites.add(ov)

        for particle in self.model.orbitSim._particles.values():
            location = self.model.orbitSim._particleLocation(particle.id)
            center = None
            if isinstance(location, OrbitNode):
                view = None
                for ov in self.node_sprites:
                    if ov.node == location:
                        view = ov
                        break
                center = ov.center
            elif isinstance(location, OrbitLink):
                view = None
                for ov in self.link_sprites:
                    if ov.link == location:
                        view = ov
                        break
                center = ov.center
            particleView = ParticleView(particle, center)
            self.particle_sprites.add(particleView)
            self.all_sprites.add(particleView)
        
                

    def drawPath(self, path, start=(0,0), xStep = 0, yStep = 0, skip = None):
        link = False
        spot = start
        for nodeId in path:
            if link:
                linkSpot = (spot[0] + xStep * self.scale, spot[1] + yStep * self.scale)
                link = self.model.orbitSim.linkById(nodeId)
                linkView = OrbitLinkView(link, spot, linkSpot)
                self.all_sprites.add(linkView)
                self.link_sprites.add(linkView)

                link = False
                continue
            else:
                if nodeId == skip:
                    link = True
                    continue
                
                spot = (spot[0] + xStep * self.scale, spot[1] + yStep * self.scale)
                node = self.model.orbitSim.nodeById(nodeId)
                if node == self.selected_node:
                    selected = True
                else:
                    selected = False
                orbitView = OrbitNodeView(node, spot, selected)
                self.all_sprites.add(orbitView)
                self.node_sprites.add(orbitView)
 
                link = True


                
    def branchPath(self, path, compare, keepJunction = True):
        branchPoint = 0
        subPath = None
        # Record all of the path beyond the point where it's identical to the longest
        for i in range(len(path)):
            if not subPath and (path[i] == compare[i]):
                branchPoint = path[i]
                continue
            elif not subPath:
                # Include the branch point so we know where to start drawing
                subPath = [branchPoint]

            subPath.append(path[i])

        return subPath

    def updateParticles(self):
        for particle in self.model.orbitSim._particles.values():
            location = self.model.orbitSim._particleLocation(particle.id)
            center = None
            if isinstance(location, OrbitNode):
                view = None
                for ov in self.node_sprites:
                    if ov.node == location:
                        view = ov
                        break
                center = ov.center
            elif isinstance(location, OrbitLink):
                view = None
                for ov in self.link_sprites:
                    if ov.link == location:
                        view = ov
                        break
                center = ov.rect.center
            
            particleView = None
            for pv in self.particle_sprites:
                if pv.particle == particle:
                    particleView = pv
                    break
            particleView.rect.center = center

    def resolveNodeClick(self, c):
        if self.target_mode:
            if isinstance(c, OrbitNodeView):
                if c.node != self.target_panel.source:
                    self.target_panel.set_target(c.node)
                    self.target_panel.update()
        else:
            if isinstance(c, OrbitNodeView):
                print(c.node.name)
                self.selected_node = c.node
                self.computeLayout()

                if self.active_summary:
                    self.active_summary.hide()

                if c.node.planet:
                    self.planet_summary.set_planet(self.model.planetSim.planetById(c.node.planet))
                    self.active_summary = self.planet_summary
                else:
                    self.active_summary = self.orbit_summary

                self.active_summary.set_node(c.node)

            elif isinstance(c, OrbitLinkView):
                if self.active_summary:
                    self.active_summary.hide()

                self.link_summary.set_link(c.link)
                self.active_summary = self.link_summary

            self.active_summary.update()
            self.active_summary.show()

    def handleShip(self, event):
        if self.ship_summary.upperAction == 1:
            location = self.ship_summary.ship_location()
            locationView = None
            for ov in self.node_sprites:
                if ov.node == location:
                    locationView = ov
                    break
            for ov in self.link_sprites:
                if ov.link  == location:
                    locationView = ov
                    break
            self.resolveNodeClick(locationView)
        elif self.ship_summary.upperAction == 2:
            self.target_panel.set_ship(self.ship_summary.ship)
            self.target_panel.set_source(self.ship_summary.ship_location())
            self.target_panel.update()
            self.target_panel.show()
            self.target_mode = True


    

 # Alternative algo:
 # - OrbitSim has a _findPath method
 # - First, traverse set of nodes to find all leaf nodes
 # - Then, from root node run findPath to each in turn.
 # - These are our paths.
 # - Literally just count lengths to find longest
 # - Rest of algo proceeds as before. 
    
    def run(self):
        returnCode = 0

        for event in pygame.event.get():
            if event.type == QUIT:
                returnCode = QUIT
                break
            elif event.type == MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()

                clicked_items = [s for s in self.all_sprites if s.rect.collidepoint(pos)]
                for c in clicked_items:
                    self.resolveNodeClick(c)

                    
            elif event.type == MOUSEWHEEL:
                if event.y == 1:
                    self.scale = max(self.scale-0.1, 0.1)
                elif event.y == -1:
                    self.scale = min(self.scale+0.1, 2.0)
                self.computeLayout()

            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    self.basePoint = (self.basePoint[0], max(self.basePoint[1]-50, self.boundsRect.top))
                elif event.key == K_DOWN:
                    self.basePoint = (self.basePoint[0], min(self.basePoint[1]+50, self.boundsRect.bottom))
                elif event.key == K_LEFT:
                    self.basePoint = (max(self.basePoint[0]-50, self.boundsRect.left), self.basePoint[1])
                elif event.key == K_RIGHT:
                    self.basePoint = (min(self.basePoint[0]+50, self.boundsRect.right), self.basePoint[1])
                self.computeLayout()

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.hello_button:
                    returnCode = LOADMENUVIEW
                    break
                elif self.active_summary and self.active_summary.handle_event(event):
                    if isinstance(self.active_summary, ShipStatusPanel):
                        self.handleShip(event)
                elif self.timing_panel.handle_event(event):
                    pass
                elif self.target_panel.handle_event(event):
                    if event.ui_element == self.target_panel.hide_button:
                        self.target_mode = False
                        self.target_panel.clear_state()
                else:
                    assert("Unknown UI element {0}".format(event.ui_element))
            elif event.type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
                if event.ui_element == self.active_summary.station_list:
                    ship = None
                    for s in self.model.orbitSim._particles.values():
                        if s.payload.name == event.text:
                            ship = s

                    assert(ship)

                    if self.active_summary:
                        self.active_summary.hide()

                    self.ship_summary.set_ship(ship)
                    self.active_summary = self.ship_summary

                    self.active_summary.update()
                    self.active_summary.show()

                    

            

            self.manager.process_events(event)

        self.screen.fill((20, 20, 120))

        self.timing_panel.update()
        self.ship_summary.update()
        self.updateParticles()

        for entity in self.all_sprites:
            self.screen.blit(entity.surf, entity.rect)

        return returnCode