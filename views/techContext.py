from views.guiContext import GUIContext

from views.panels import TechStatusPanel

from techtree import (
    TechNode,
    TechTree,
)

from gameModel import GameModel

import pygame

from pygame.locals import (
    QUIT,
    MOUSEBUTTONUP,
)


class TechView(pygame.sprite.Sprite):
    def __init__(self, tech: TechNode, center: tuple[int, int]=(0,0)):
        super(TechView, self).__init__()
        self.center = center
        self.tech = tech
        self.surf = pygame.surface.Surface((200, 100))
        self.surf.set_colorkey((0, 0, 0))
        color = (150, 250, 100)
        pygame.draw.rect(self.surf, color, (0, 0, 200, 100))

        font = pygame.font.Font(size=16)
        text = font.render(self.tech.name, True, (128, 128, 230))
        textRect = text.get_rect()
        textRect.center = (100, 25)

        self.surf.blit(text, textRect)

        self.rect = self.surf.get_rect(center=self.center)




class TechContext(GUIContext):
    def __init__(self, screen, model: GameModel, manager, ):
        super(TechContext, self).__init__(screen, model, manager)
        self.all_sprites = pygame.sprite.Group()

        self.techTree = model.techTree

        x = 150
        y = 100
        for tech in self.techTree.nodes.values():
            self.all_sprites.add(TechView(tech, (x, y)))
            x += 250
            if x >= 800:
                x = 150
                y += 150

        summary_rect = pygame.Rect(800, 200, 400, 600)


        self.tech_panel = TechStatusPanel(summary_rect, manager, model)
        self.tech_panel.hide()
        
    def resolveNodeClick(self, item):
        if isinstance(item, TechView):
            self.tech_panel.tech = item.tech
            self.tech_panel.update()
            self.tech_panel.show()

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
                for item in clicked_items:
                    self.resolveNodeClick(item)      

                if not clicked_items:
                    self.tech_panel.tech = None
                    self.tech_panel.hide()    

            self.manager.process_events(event)


        self.screen.fill((140, 0, 25))

        for entity in self.all_sprites:
            self.screen.blit(entity.surf, entity.rect)

        return returnCode
