from views.guiContext import GUIContext

from views.panels import TechStatusPanel, TechProgressPanel, TimingPanel

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
from pygame.event import Event
from pygame_gui.elements import UIButton
from pygame_gui import (
    UI_BUTTON_PRESSED,
)

from views.guiContext import GUICode

class TechView(pygame.sprite.Sprite):
    def __init__(self, tech: TechNode, center: tuple[int, int]=(0,0), tier=-1, selected=False, discovered=False, available=False):
        super(TechView, self).__init__()
        self.center = center
        self.tech = tech
        self.tier = tier
        self.surf = pygame.surface.Surface((200, 100))
        self.surf.set_colorkey((0, 0, 0))
        if selected:
            color = (200, 200, 50)
        elif discovered:
            color = (150, 250, 100)
        elif available:
            color = (50, 250, 250)
        else:
            color = (150, 150, 150)
        pygame.draw.rect(self.surf, color, (0, 0, 200, 100))

        font = pygame.font.Font(size=16)
        text = font.render(self.tech.name, True, (128, 128, 230))
        textRect = text.get_rect()
        textRect.center = (100, 25)

        self.surf.blit(text, textRect)

        self.rect = self.surf.get_rect(center=self.center)


class SimpleLink(pygame.sprite.Sprite):
    def __init__(self, startPos: tuple[int, int]=(200,200)):
        super(SimpleLink, self).__init__()
        self.startPos = startPos
        self.surf = pygame.surface.Surface((100,100))
        self.surf.set_colorkey((0,0,0))
        pygame.draw.circle(self.surf, (100, 100, 100), center=(20, 20), radius=20)
        self.rect = self.surf.get_rect(center = startPos)


class TechLink(pygame.sprite.Sprite):
    def __init__(self, startPos: tuple[int, int]=(0,0), endPos: tuple[int, int]=(0,0)):
        super(TechLink, self).__init__()
        self.startPos = startPos
        self.endPos = endPos 
        
        xDiff = endPos[0] - startPos[0]
        yDiff = endPos[1] - startPos[1]


        if abs(xDiff) < 10:
            self.surf = pygame.surface.Surface((10, abs(yDiff)))
        else:
            self.surf = pygame.surface.Surface(
               (
                   abs(xDiff),
                   abs(yDiff),
               )
            )
        self.surf.set_colorkey((0,0,0))
        import random
        color = (50, 100, 250)

        if xDiff >= 0:
            pygame.draw.line(self.surf, color, (0,0), (xDiff, yDiff), width = 5)
        else:
            pygame.draw.line(self.surf, color, (abs(xDiff), 0), (0, yDiff), width = 5)

        if xDiff >= 0:
            left = startPos[0]
        else:
            left = endPos[0]
        self.rect = self.surf.get_rect(left = left, top = startPos[1])







class TechContext(GUIContext):
    def __init__(self, screen, model: GameModel, manager, boundsRect=pygame.Rect(-100, -100, 1400, 2000)):
        super(TechContext, self).__init__(screen, model, manager)
        self.tech_sprites = pygame.sprite.Group()
        self.link_sprites = pygame.sprite.Group()

        self.techTree = model.techTree
        self.playerTech = model.playerTech

        self.selectedTech = None


        self.boundsRect = boundsRect

        self.basePoint = (150, 700)
        self.computeLayout()

        self.orbit_button = UIButton(
            relative_rect=pygame.Rect((0, 0), (100, 50)),
            text="Orbit Map",
            manager=manager,
        )

        summary_rect = pygame.Rect(800, 100, 400, 800)
        progress_rect = pygame.Rect(600, 0, 200, 50)
        timing_rect = pygame.Rect(800, 0, 400, 100)


        self.tech_panel = TechStatusPanel(summary_rect, manager, model)
        self.tech_panel.hide()

        self.progress_panel = TechProgressPanel(progress_rect, manager, playerTech=model.playerTech)
        self.progress_panel.update()

        self.timing_panel = TimingPanel(
            timing_rect, manager=manager, timingMaster=self.model.timingMaster
        )

    def computeLayout(self):
        self.tech_sprites.empty()
        self.link_sprites.empty()
        (x, y) = self.basePoint
        tierNodes = {}
        for tech in self.techTree.nodes.values():
            tier = self.computeTier(tech)
            if tier in tierNodes:
                tierNodes[tier] += 1
            else:
                tierNodes[tier] = 0
            spritePos = (self.basePoint[0] + 350*tierNodes[tier] + 125 * (tier % 2),
                        self.basePoint[1] - 250*tier)
            if self.selectedTech == tech:            
                self.tech_sprites.add(TechView(tech, spritePos, tier, selected = True))
            elif tech.id in self.playerTech.discoveredTechs:
                self.tech_sprites.add(TechView(tech, spritePos, tier, discovered=True))
            elif tech.id in self.playerTech.possibleTargets:
                self.tech_sprites.add(TechView(tech, spritePos, tier, available=True))
            else:
                self.tech_sprites.add(TechView(tech, spritePos, tier))
                        

        for tv in self.tech_sprites:
            for a in tv.tech.ancestors:
                tech = self.techTree.nodeById(a)
                sprite = self.techSpriteForTech(tech)
                startPos = tv.rect.center
                endPos = sprite.rect.center
                linkSprite = TechLink((startPos[0], startPos[1]+50), (endPos[0], endPos[1]-50))
                self.link_sprites.add(linkSprite)

    def techSpriteForTech(self, tech):
        sprite = None
        for t in self.tech_sprites:
            if t.tech == tech:
                sprite = t
        return sprite
            

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
            self.selectedTech = item.tech
            self.tech_panel.tech = self.selectedTech
            self.tech_panel.update()
            self.tech_panel.show()
            self.computeLayout()

    def handleMouseClick(self, event: Event) -> None:
        pos = pygame.mouse.get_pos()

        if self.tech_panel.rect.collidepoint(pos):
            return
        
        if self.timing_panel.rect.collidepoint(pos):
            return

        clicked_items = [
            s for s in self.tech_sprites if s.rect.collidepoint(pos)
        ]             
        for item in clicked_items:
            self.resolveNodeClick(item)      

        if not clicked_items:
            self.tech_panel.tech = None
            self.tech_panel.hide()    
            self.selectedTech = None
            self.computeLayout()

    def handleGuiButton(self, event: Event) -> GUICode:
        if event.ui_element == self.orbit_button:
            return GUICode.LOADORBITVIEW
        elif event.ui_element == self.tech_panel.research_button:
            self.playerTech.setActiveTech(self.selectedTech.id)
            self.progress_panel.update()
        elif self.timing_panel.handle_event(event):
            pass
        return 0

    def run(self):
        returnCode = 0

        for event in pygame.event.get():
            if event.type == QUIT:
                returnCode = QUIT
                break
            elif event.type == KEYDOWN:
                self.handleKeyPress(event)

            elif event.type == MOUSEBUTTONUP:
                self.handleMouseClick(event)

            elif event.type == UI_BUTTON_PRESSED:
                returnCode = self.handleGuiButton(event)
                if returnCode != 0:
                    break

            self.manager.process_events(event)

        self.screen.fill((140, 0, 25))

        for tv in self.link_sprites:
            self.screen.blit(tv.surf, tv.rect)
        for entity in self.tech_sprites:
            self.screen.blit(entity.surf, entity.rect)

        self.timing_panel.update()
        self.tech_panel.update()
        self.progress_panel.update()

        return returnCode
