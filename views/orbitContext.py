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
        pygame.draw.circle(self.surf, (255, 255, 100, 100), (10, 10), 10.0)

        self.rect = self.surf.get_rect(center = self.center)



class OrbitContext(GUIContext):
    def __init__(self, screen, model):
        super(OrbitContext, self).__init__(screen, model)
        orbitSpot = (400, 750)
        self.all_sprites = pygame.sprite.Group()

        # First label root node. By convention node 0 (surface of sun)
        rootNode = model.orbitSim.nodeById(0)
        terminalNode = model.orbitSim.nodeById(99)

        longestPath = model.orbitSim._findPath(rootNode.id, terminalNode.id, [])[0]

        # Then find all planet leaf nodes
        leafNodes = []
        for node in model.orbitSim._nodes.values():
            if (node.leaf == LeafClass.PLANET and node.id != 0):
                leafNodes.append(node)

        # Then find all paths from root to leaves
        paths = [model.orbitSim._findPath(rootNode.id, node.id, [])[0] for node in leafNodes]

        # Find the longest - this will be our "trunk"
        #longestPathLength = 0
        #longestPath = paths[0]
        #for path in paths:
        #    if len(path) > longestPathLength:
        #        longestPathLength = len(path)
        #        longestPath = path

        # Draw trunk - path is node/link/node/link/node so just skip links for now
        link = False
        for nodeId in longestPath:
            if link:
                link = False
                continue
            else:
                link = True

            node = model.orbitSim.nodeById(nodeId)
            orbitView = OrbitNodeView(node, orbitSpot)
            self.all_sprites.add(orbitView)
            orbitSpot = (orbitSpot[0], orbitSpot[1] - 70)

        # Now do branches - first find all the paths that aren't the longest
        branchPaths = []
        for path in paths:
            if path is longestPath:
                continue

            branchPoint = 0
            subPath = None
            # Record all of the path beyond the point where it's identical to the longest
            for i in range(len(path)):
                if not subPath and (path[i] == longestPath[i]):
                    branchPoint = path[i]
                    continue
                elif not subPath:
                    # Include the branch point so we know where to start drawing
                    subPath = [branchPoint]

                subPath.append(path[i])

            branchPaths.append(subPath)

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

            # Now draw them as before, but stepping horizontally
            link = False
            for nodeId in path:
                if link:
                    link = False
                    continue
                else:
                    link = True

                # Skip the branch point as this has already been drawn by the trunk code
                if nodeId == branchPoint:
                    continue

                branchRoot = (branchRoot[0] + (reverse*60), branchRoot[1])
                node = model.orbitSim.nodeById(nodeId)
                orbitView = OrbitNodeView(node, branchRoot)
                self.all_sprites.add(orbitView)
        
        # Now handle moons
        moonNodes = []
        for node in model.orbitSim._nodes.values():
            if (node.leaf == LeafClass.MOON and node.id != 0):
                moonNodes.append(node)

        moonPaths = [model.orbitSim._findPath(rootNode.id, node.id, [])[0] for node in moonNodes]

        for moonPath in moonPaths:
            # First work out which planet this moon belongs to
            branchPoint = 0
            subPath = None
            # Strip off the main trunk
            for i in range(len(moonPath)):
                if not subPath and (moonPath[i] == longestPath[i]):
                    branchPoint = moonPath[i]
                    continue
                elif not subPath:
                    # Include the branch point so we know where to start drawing
                    subPath = [branchPoint]

                subPath.append(moonPath[i])
            
            # Now find the right branch
            moonBranch = 0
            subSubPath = None
            for branch in branchPaths:
                if branch[0] != subPath[0]:
                    continue

                # Then repeat to find the branch from the planet's path
                for i in range(len(subPath)):
                    if not subSubPath and (subPath[i] == branch[i]):
                        moonBranch = subPath[i]
                        continue
                    elif not subSubPath:
                        subSubPath = [moonBranch]

                    subSubPath.append(subPath[i])

            moonSpot = (0,0)
            for ov in self.all_sprites:
                if ov.node.id == subSubPath[0]:
                    moonSpot = ov.center

            link = False
            for nodeId in subSubPath:
                if link:
                    link = False
                    continue
                else:
                    link = True

                if nodeId == moonBranch:
                    continue

                moonSpot = (moonSpot[0], moonSpot[1] + 30)
                node = model.orbitSim.nodeById(nodeId)
                orbitView = OrbitNodeView(node, moonSpot)
                self.all_sprites.add(orbitView)
                

            
                






 # Layout algorithm:
 # - Pick a node to be root node (probably convention to be node 0 as this is surface of sun)
 # - Make a list of paths from root node:
 # - For each unwalked link:
 #   - If only one onward link, add to path and continue
 #   - If multiple onward, branch - make a new path and iterate on that
 #   - If no onward, terminate recursion
 # - Once made, find longest path:
 #   - Compare branches at each branch point and transpose if needed
 # - For longest path, space nodes vertically
 # - For each subpath, space nodes horizontally       

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