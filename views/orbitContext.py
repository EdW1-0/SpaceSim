import pygame
import pygame_gui
from pygame_gui.elements import UIButton, UIImage, UILabel
from pygame_gui.core import UIContainer

from views.guiContext import GUIContext

from orbitsim.orbitNode import LeafClass

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
        pygame.draw.rect(self.surf, (200, 50, 50), (0, 0, width, height))
        self.rect = self.surf.get_rect(top = top, left=left)

class PlanetStatusPanel:
    def __init__(self, rect, manager=None):
        self.rect = rect
        self.container = UIContainer(rect, manager = manager)
        background = pygame.Surface((rect.width,rect.height))
        pygame.draw.rect(background, (10, 10, 10), (0, 0, rect.width, rect.height))
        self.background = UIImage((0,0,rect.width,rect.height), background, manager = manager, container=self.container)

        self.planet_name_label = UILabel(pygame.Rect(0,0,rect.width, 100), 
                                         text="Planet placeholder", 
                                         manager=manager, 
                                         container=self.container)
        
        planet_image = pygame.Surface((50, 50))
        pygame.draw.circle(planet_image, (200,200,10),(25,25), 25)
        self.planet_image = UIImage(pygame.Rect(50, 100, 50, 50), planet_image, manager=manager, container=self.container)

        self.hide_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0,0), (20, 20)), text='X', container=self.container, manager=manager)

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
        
    def set_node(self, node):
        self.node = node

    def update(self):
        self.planet_name_label.set_text(self.node.name)


class OrbitContext(GUIContext):
    def __init__(self, screen, model, manager, boundsRect = pygame.Rect(-100, -100, 1400, 2000)):
        super(OrbitContext, self).__init__(screen, model, manager)
        self.all_sprites = pygame.sprite.Group()
        self.node_sprites = pygame.sprite.Group()
        self.link_sprites = pygame.sprite.Group()

        self.selected_node = None

        self.boundsRect = boundsRect
        self.scale = 1.0
        self.basePoint = (400, 750)

        self.computeLayout()

        self.hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 0), (100, 50)),
                                             text='Settings',
                                             manager=manager)

        
        self.planet_summary = PlanetStatusPanel(pygame.Rect(800, 200, 400, 600), manager=manager)
        #self.planet_window.add_element(self.boop_button)
        self.planet_summary.hide()

    def computeLayout(self):
        self.all_sprites.empty()
        self.node_sprites.empty()
        self.link_sprites.empty()

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
                    if isinstance(c, OrbitNodeView):
                        print(c.node.name)
                        self.selected_node = c.node

                        self.planet_summary.set_node(c.node)
                        self.planet_summary.update()
                        self.planet_summary.show()

                        self.computeLayout()
                        
                    elif isinstance(c, OrbitLinkView):
                        print(c.link.topNode, c.link.bottomNode)
                    
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
                elif self.planet_summary.handle_event(event):
                    pass
                else:
                    assert("Unknown UI element {0}".format(event.ui_element))

            self.manager.process_events(event)

        self.screen.fill((20, 20, 120))

        for entity in self.all_sprites:
            self.screen.blit(entity.surf, entity.rect)

        return returnCode