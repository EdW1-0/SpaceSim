from views.guiContext import GUIContext

from techtree import (
    TechNode,
    TechTree,
)

from gameModel import GameModel

import pygame

from pygame.locals import (
    QUIT,
)


class TechView(pygame.sprite.Sprite):
    def __init__(self, tech: TechNode, center: tuple[int, int]=(0,0)):
        super(TechView, self).__init__()
        self.center = center
        self.tech = tech
        self.surf = pygame.surface.Surface((100, 60))
        self.surf.set_colorkey((0, 0, 0))
        color = (150, 250, 100)
        pygame.draw.rect(self.surf, color, (0, 0, 100, 60))
        self.rect = self.surf.get_rect(center=self.center)




class TechContext(GUIContext):
    def __init__(self, screen, model: GameModel, manager, ):
        super(TechContext, self).__init__(screen, model, manager)
        self.all_sprites = pygame.sprite.Group()

        self.all_sprites.add(TechView(None, (300, 300)))

        pass


    def run(self):
        returnCode = 0

        for event in pygame.event.get():
            if event.type == QUIT:
                returnCode = QUIT
                break
                        
            self.manager.process_events(event)


        self.screen.fill((140, 0, 25))

        for entity in self.all_sprites:
            self.screen.blit(entity.surf, entity.rect)

        return returnCode
