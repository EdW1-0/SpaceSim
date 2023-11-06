import pygame


from views.guiContext import GUIContext, GUICode
from views.timingView import TimingPanel
from views.orbitViews.orbitViews import (
    OrbitNodeView,
    OrbitNodeViewLabel,
    OrbitLinkView,
    OrbitLinkViewLabel,
    ParticleView,
)
from views.sidePanels.sideStatusPanel import (
    OrbitStatusPanel,
    LinkStatusPanel,
    PlanetStatusPanel,
    TargetSettingPanel,
    ShipStatusPanel,
)

from orbitsim.orbitNode import LeafClass, OrbitNode
from orbitsim.orbitLink import OrbitLink
from orbitsim.orbitTrajectory import TrajectoryState

from planetsim.planet import Planet
from colonysim.colony import Colony

from views.surfaceContext import SCMode

from views.routingModeInfo import RoutingModeInfo




from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    KEYDOWN,
    MOUSEBUTTONUP,
    MOUSEWHEEL,
    QUIT,
)

from pygame_gui.elements import UIButton
from pygame_gui import UI_BUTTON_PRESSED, UI_SELECTION_LIST_NEW_SELECTION

from enum import Enum


class OCMode(str, Enum):
    Standard = "Standard"
    Target = "Target"
    LaunchPlan = "LaunchPlan"


class OrbitContext(GUIContext):
    def __init__(
        self,
        screen,
        model,
        manager,
        boundsRect=pygame.Rect(-100, -100, 1400, 2000),
        mode = OCMode.Standard,
        info=None,
    ):
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

        self.hello_button = UIButton(
            relative_rect=pygame.Rect((0, 0), (100, 50)),
            text="Settings",
            manager=manager,
        )

        summary_rect = pygame.Rect(800, 200, 400, 600)
        timing_rect = pygame.Rect(800, 0, 400, 200)
        target_rect = pygame.Rect(400, 500, 400, 300)

        self.planet_summary = PlanetStatusPanel(
            summary_rect, manager=manager, model=self.model
        )
        # self.planet_window.add_element(self.boop_button)
        self.planet_summary.hide()

        self.orbit_summary = OrbitStatusPanel(
            summary_rect, manager=manager, model=self.model
        )
        self.orbit_summary.hide()

        self.link_summary = LinkStatusPanel(summary_rect, manager=manager)
        self.link_summary.hide()

        self.ship_summary = ShipStatusPanel(
            summary_rect, manager=manager, model=self.model
        )
        self.ship_summary.hide()

        self.active_summary = None

        self.target_panel = TargetSettingPanel(
            target_rect, manager=manager, model=self.model
        )
        self.target_panel.hide()

        self.timing_panel = TimingPanel(
            timing_rect, manager=manager, timingMaster=self.model.timingMaster
        )

        self.target_mode = mode
        self.info = info

        if self.target_mode == OCMode.Target:
            self.ship_summary.set_ship(self.info.ship)
            self.ship_summary.show()
            self.active_summary = self.ship_summary
            self.target_panel.set_ship(self.info.ship)
            self.target_panel.set_source(self.ship_summary.ship_location())
            self.target_panel.set_target(self.info.end)
            if self.info.surfaceCoordinates:
                self.target_panel.set_coordinates(self.info.surfaceCoordinates)
            self.target_panel.show()
        elif self.target_mode == OCMode.LaunchPlan:
            # Get source - this will be colony or planet ship is on.
            # In fact the node this is associated with.
            # Can get this from colony locale - surface.
            # Go through planetsim to look up relevant planet
            # Then go through orbitsim to look up relevant node.
            if isinstance(self.info.start, Colony):
                colony = self.info.start

                locale = colony.locale
                planet = None
                for p in model.planetSim.planets.values():
                    if p.surface == locale:
                        planet = p
            elif isinstance(self.info.start, Planet):
                planet = self.info.start
            else:
                print("Insufficient information to find planet:", self.info)
                assert False

            node = None
            for n in model.orbitSim._nodes.values():
                if n.planet == planet.id:
                    node = n

            self.target_panel.set_source(node)
            self.target_panel.set_ship(self.info.ship)
            # TODO: This is a hack. Trajectory should really be managed by
            # particle and looked up by view, not created.
            if self.info.trajectory:
                self.target_panel.trajectory = self.info.trajectory
            if self.info.end:
                self.target_panel.set_target(self.info.end)
            if self.info.surfaceCoordinates:
                self.target_panel.set_coordinates(self.info.surfaceCoordinates)
            self.target_panel.update()
            self.target_panel.show()

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
        self.drawPath(trunkPath, start=sunSpot, yStep=-140)

        # Then find all planet leaf nodes
        planetNodes = []
        for node in self.model.orbitSim._nodes.values():
            if node.leaf == LeafClass.PLANET and node.id != 0:
                planetNodes.append(node)

        # Then find all paths from root to leaves
        planetPaths = [
            self.model.orbitSim._findPath(rootNode.id, node.id, [])[0]
            for node in planetNodes
        ]
        branchPaths = [self.branchPath(path, trunkPath) for path in planetPaths]

        # Now draw the branch.
        count = 0
        for path in branchPaths:
            # Start by finding the view for the branch point,
            # so we know what height to draw from
            branchPoint = path[0]
            branchRoot = (0, 0)
            for ov in self.node_sprites:
                if ov.node.id == branchPoint:
                    branchRoot = ov.center

            # Alternate the direction of drawing
            reverse = 2 * (count % 2) - 1
            count += 1

            self.drawPath(path, start=branchRoot, xStep=reverse * 120, skip=branchPoint)

        # Now handle moons
        moonNodes = []
        for node in self.model.orbitSim._nodes.values():
            if node.leaf == LeafClass.MOON and node.id != 0:
                moonNodes.append(node)

        moonPaths = [
            self.model.orbitSim._findPath(rootNode.id, node.id, [])[0]
            for node in moonNodes
        ]
        moonFromTrunkPaths = [self.branchPath(path, trunkPath) for path in moonPaths]

        for moonPath in moonFromTrunkPaths:
            # Now find the right branch
            moonSubPath = None
            for branch in branchPaths:
                if branch[0] != moonPath[0]:
                    continue

                moonSubPath = self.branchPath(moonPath, branch)

            moonSpot = (0, 0)
            moonRoot = moonSubPath[0]
            for ov in self.node_sprites:
                if ov.node.id == moonRoot:
                    moonSpot = ov.center

            self.drawPath(moonSubPath, start=moonSpot, yStep=60, skip=moonRoot)

        for view in self.node_sprites:
            ov = OrbitNodeViewLabel(view.node, (view.center[0], view.center[1] + 15))
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
                center = ov.rect.center
            particleView = ParticleView(particle, center)
            self.particle_sprites.add(particleView)
            self.all_sprites.add(particleView)

    def drawPath(self, path, start=(0, 0), xStep=0, yStep=0, skip=None):
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

    def branchPath(self, path, compare, keepJunction=True):
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
                center = view.center
            elif isinstance(location, OrbitLink):
                view = None
                for ov in self.link_sprites:
                    if ov.link == location:
                        view = ov
                        break
                center = view.rect.center

            particleView = None
            for pv in self.particle_sprites:
                if pv.particle == particle:
                    particleView = pv
                    break
            # TODO: This is a kludge due to not having handled particle
            # creation/destruction properly at the GUI level, which we ought to do.
            if not particleView:
                self.computeLayout()
                return

            particleView.rect.center = center

    def resolveNodeClick(self, c):
        if self.target_mode == OCMode.Target or self.target_mode == OCMode.LaunchPlan:
            if isinstance(c, OrbitNodeView):
                if c.node != self.target_panel.source:
                    self.target_panel.set_target(c.node)
                    self.target_panel.update()
        elif isinstance(c, OrbitLinkViewLabel) or isinstance(c, OrbitNodeViewLabel):
            return
        else:
            if isinstance(c, OrbitNodeView):
                print(c.node.name)
                self.selected_node = c.node
                self.computeLayout()

                if self.active_summary:
                    self.active_summary.hide()

                if c.node.planet:
                    self.planet_summary.set_planet(
                        self.model.planetSim.planetById(c.node.planet)
                    )
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
                if ov.link == location:
                    locationView = ov
                    break
            self.resolveNodeClick(locationView)
        elif self.ship_summary.upperAction == 2:
            self.target_panel.set_ship(self.ship_summary.ship)
            self.target_panel.set_source(self.ship_summary.ship_location())
            self.target_panel.show()
            self.target_panel.update()
            self.target_mode = OCMode.Target

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

                clicked_items = [
                    s for s in self.all_sprites if s.rect.collidepoint(pos)
                ]
                for c in clicked_items:
                    self.resolveNodeClick(c)

            elif event.type == MOUSEWHEEL:
                if event.y == 1:
                    self.scale = max(self.scale - 0.1, 0.1)
                elif event.y == -1:
                    self.scale = min(self.scale + 0.1, 2.0)
                self.computeLayout()

            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    self.basePoint = (
                        self.basePoint[0],
                        max(self.basePoint[1] - 50, self.boundsRect.top),
                    )
                elif event.key == K_DOWN:
                    self.basePoint = (
                        self.basePoint[0],
                        min(self.basePoint[1] + 50, self.boundsRect.bottom),
                    )
                elif event.key == K_LEFT:
                    self.basePoint = (
                        max(self.basePoint[0] - 50, self.boundsRect.left),
                        self.basePoint[1],
                    )
                elif event.key == K_RIGHT:
                    self.basePoint = (
                        min(self.basePoint[0] + 50, self.boundsRect.right),
                        self.basePoint[1],
                    )
                self.computeLayout()

            if event.type == UI_BUTTON_PRESSED:
                if event.ui_element == self.hello_button:
                    returnCode = GUICode.LOADMENUVIEW
                    break
                elif self.active_summary and self.active_summary.handle_event(event):
                    if isinstance(self.active_summary, ShipStatusPanel):
                        self.handleShip(event)
                    elif isinstance(self.active_summary, PlanetStatusPanel):
                        if self.planet_summary.upperAction == 1:
                            self.upperContext = {
                                "planet": self.planet_summary.planet.id
                            }
                            returnCode = GUICode.LOADSURFACEVIEW
                            break
                elif self.timing_panel.handle_event(event):
                    pass
                elif self.target_panel.handle_event(event):
                    if (
                        event.ui_element == self.target_panel.hide_button
                        or self.target_panel.upperAction == 1
                    ):
                        if self.target_mode == OCMode.Target:
                            self.target_mode = OCMode.Standard
                            self.target_panel.trajectory.state = TrajectoryState.PENDING
                            self.target_panel.clear_state()
                        elif self.target_mode == OCMode.LaunchPlan:
                            if isinstance(self.info.start, Colony):
                                self.info.trajectory = self.target_panel.trajectory
                                self.info.end = self.target_panel.target
                                returnCode = GUICode.LOADCOLONYVIEW_LAUNCH_RETURN
                            elif isinstance(self.info.start, Planet):
                                self.info.trajectory = self.target_panel.trajectory
                                self.info.end = self.target_panel.target
                                returnCode = GUICode.LOADSURFACEVIEW_LAUNCH_RETURN
                            break
                    elif self.target_panel.upperAction == 2:
                        if not self.info:
                            self.info = RoutingModeInfo()
                            self.info.start = self.target_panel.source
                            self.info.ship = self.target_panel.ship
                        self.info.end = self.target_panel.target
                        if self.target_panel.trajectory:
                            self.info.trajectory = self.target_panel.trajectory
                        returnCode = GUICode.LOADSURFACEVIEW_LANDING_PLAN
                        break
                else:
                    assert "Unknown UI element {0}".format(event.ui_element)
            elif event.type == UI_SELECTION_LIST_NEW_SELECTION:
                if event.ui_element == self.active_summary.station_list:
                    ship = None
                    for s in self.model.orbitSim._particles.values():
                        if s.payload.name == event.text:
                            ship = s

                    assert ship

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
