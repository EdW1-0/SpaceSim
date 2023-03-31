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



class OrbitContext(GUIContext):
    def __init__(self, screen, model):
        super(OrbitContext, self).__init__(screen, model)
        self.all_sprites = pygame.sprite.Group()
        self.model = model
        self.screen = screen
        self.draw()

    def draw(self):
        # First label root node. By convention node 0 (surface of sun)
        rootNode = self.model.orbitSim.nodeById(0)
        terminalNode = self.model.orbitSim.nodeById(99)
        sunSpot = (400, 750)

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
            for ov in self.all_sprites:
                if ov.node.id == branchPoint:
                    branchRoot = ov.center

            # Alternate the direction of drawing
            if count % 2:
                reverse = 1
            else:
                reverse = -1
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
            for ov in self.all_sprites:
                if ov.node.id == moonRoot:
                    moonSpot = ov.center

            self.drawPath(moonSubPath, start = moonSpot, yStep = 30, skip = moonRoot)
                

    def drawPath(self, path, start=(0,0), xStep = 0, yStep = 0, skip = None):
        link = False
        spot = start
        for nodeId in path:
            if link:
                link = False
                continue
            else:
                link = True

            if nodeId == skip:
                continue

            spot = (spot[0] + xStep, spot[1] + yStep)
            node = self.model.orbitSim.nodeById(nodeId)
            orbitView = OrbitNodeView(node, spot)
            self.all_sprites.add(orbitView)
                
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
                    print(c.node.name)
                    

                if pos[0] < 50 and pos[1] < 50:
                    print ("foo")
                    returnCode = LOADMENUVIEW
                    break

        self.screen.fill((20, 20, 120))

        surf = pygame.surface.Surface((50, 50))
        pygame.draw.rect(self.screen, (10, 10, 10), pygame.Rect(0, 0, 50, 50))

        for entity in self.all_sprites:
            self.screen.blit(entity.surf, entity.rect)

        return returnCode