from views.guiContext import GUIContext

from orbitsim.orbitNode import LeafClass

import pygame

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
    def __init__(self, node, center=(0, 0)):
        super(OrbitNodeView, self).__init__()
        self.center = center
        self.node = node
        self.surf = pygame.surface.Surface((20, 20))
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
        pygame.draw.circle(self.surf, color, (10, 10), 10.0)

        self.rect = self.surf.get_rect(center = self.center)

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
        
        self.start = start
        self.end = end
        self.link = link
        self.surf = pygame.surface.Surface((width, height))
        self.surf.set_colorkey((0, 0, 0))
        pygame.draw.rect(self.surf, (200, 50, 50), (0, 0, width, height))
        self.rect = self.surf.get_rect(top = top, left=left)

class OrbitContext(GUIContext):
    def __init__(self, screen, model, boundsRect = pygame.Rect(-100, -100, 1400, 1000)):
        super(OrbitContext, self).__init__(screen, model)
        self.all_sprites = pygame.sprite.Group()
        self.node_sprites = pygame.sprite.Group()
        self.link_sprites = pygame.sprite.Group()
        self.model = model
        self.screen = screen
        self.boundsRect = boundsRect
        self.scale = 1.0
        self.basePoint = (400, 750)

        self.computeLayout()

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
        self.drawPath(trunkPath, start = sunSpot, yStep = -70)


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

            self.drawPath(path, start = branchRoot, xStep = reverse*60, skip = branchPoint)

        
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

            self.drawPath(moonSubPath, start = moonSpot, yStep = 30, skip = moonRoot)
                

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
                orbitView = OrbitNodeView(node, spot)
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
                    elif isinstance(c, OrbitLinkView):
                        print(c.link.topNode, c.link.bottomNode)
                    

                if pos[0] < 50 and pos[1] < 50:
                    returnCode = LOADMENUVIEW
                    break

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

        self.screen.fill((20, 20, 120))

        surf = pygame.surface.Surface((50, 50))
        pygame.draw.rect(self.screen, (10, 10, 10), pygame.Rect(0, 0, 50, 50))

        for entity in self.all_sprites:
            self.screen.blit(entity.surf, entity.rect)

        return returnCode