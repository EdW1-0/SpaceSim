import pygame

from orbitsim.orbitNode import LeafClass

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
