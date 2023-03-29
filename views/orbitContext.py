from views.guiContext import GUIContext

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

class OrbitNode(pygame.sprite.Sprite):
    def __init__(self, node, center=(0, 0)):
        super(OrbitNode, self).__init__()
        self.center = center
        self.node = node
        self.surf = pygame.surface.Surface((20, 20))
        self.surf.set_colorkey((0, 0, 0))
        pygame.draw.circle(self.surf, (255, 255, 100, 100), (10, 10), 10.0)

        self.rect = self.surf.get_rect(center = self.center)



class OrbitContext(GUIContext):
    def __init__(self, screen, model):
        super(OrbitContext, self).__init__(screen, model)
        orbitSpot = (200, 550)
        self.all_sprites = pygame.sprite.Group()

        # First label root node. By convention node 0 (surface of sun)
        rootNode = model.orbitSim.nodeById(0)
        # Then find all leaf nodes
        leafNodes = []
        for node in model.orbitSim._nodes.values():
            if (len(node.links) == 1 and node.id != 0):
                leafNodes.append(node)

        # Then find all paths from root to leaves
        paths = [model.orbitSim._findPath(rootNode.id, node.id, [])[0] for node in leafNodes]

        # Find the longest - this will be our "trunk"
        longestPathLength = 0
        longestPath = paths[0]
        for path in paths:
            if len(path) > longestPathLength:
                longestPathLength = len(path)
                longestPath = path

        # Draw trunk - path is node/link/node/link/node so just skip links for now
        link = False
        for nodeId in longestPath:
            if link:
                link = False
                continue
            else:
                link = True

            node = model.orbitSim.nodeById(nodeId)
            orbitView = OrbitNode(node, orbitSpot)
            self.all_sprites.add(orbitView)
            orbitSpot = (orbitSpot[0], orbitSpot[1] - 40)





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