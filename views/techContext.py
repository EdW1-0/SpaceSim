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
    KEYDOWN,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
)


class TechView(pygame.sprite.Sprite):
    def __init__(self, tech: TechNode, center: tuple[int, int]=(0,0), tier=-1):
        super(TechView, self).__init__()
        self.center = center
        self.tech = tech
        self.tier = tier
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
    def __init__(self, screen, model: GameModel, manager, boundsRect=pygame.Rect(-100, -100, 1400, 2000)):
        super(TechContext, self).__init__(screen, model, manager)
        self.all_sprites = pygame.sprite.Group()

        self.techTree = model.techTree

        self.boundsRect = boundsRect

        self.basePoint = (150, 700)
        self.computeLayout()

        summary_rect = pygame.Rect(800, 200, 400, 600)


        self.tech_panel = TechStatusPanel(summary_rect, manager, model)
        self.tech_panel.hide()

    def computeLayout(self):
        self.all_sprites.empty()
        (x, y) = self.basePoint
        tierNodes = {}
        for tech in self.techTree.nodes.values():
            tier = self.computeTier(tech)
            if tier in tierNodes:
                tierNodes[tier] += 1
            else:
                tierNodes[tier] = 0
            self.all_sprites.add(TechView(tech, (self.basePoint[0] + 250*tierNodes[tier], self.basePoint[1] - 150*tier), tier))
            

    def computeTier(self, tech):
        def ancestorDepth(tech: TechNode, techTree: TechTree):
            if not tech.ancestors:
                return 0
            
            maxDepth = 0
            for ancestor in tech.ancestors:
                depth = ancestorDepth(techTree.nodeById(ancestor), techTree) + 1
                if depth > maxDepth:
                    maxDepth = depth

            return maxDepth
        
        return ancestorDepth(tech, self.techTree)


    def handleKeyPress(self, event: pygame.event.Event):
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
            elif event.type == KEYDOWN:
                self.handleKeyPress(event)

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
