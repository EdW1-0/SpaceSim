from views.guiContext import GUIContext

import pygame

from pygame.locals import (
    MOUSEBUTTONUP,
    QUIT,
)

from views.guiContext import GUICode

from gameModel import GameModel

from tkinter import simpledialog, filedialog


class MenuItem(pygame.sprite.Sprite):
    def __init__(self, center=(0, 0), text="Default", handler=None):
        super(MenuItem, self).__init__()
        self.text = text
        if handler:
            self.handler = handler
        else:
            self.handler = self.click
        self.surf = pygame.surface.Surface((100, 50))
        pygame.draw.rect(self.surf, (10, 10, 10), pygame.Rect(0, 0, 100, 50))

        font = pygame.font.Font(size=20)
        text = font.render(self.text, True, (128, 128, 230))
        textRect = text.get_rect()
        textRect.center = (50, 25)

        self.surf.blit(text, textRect)

        self.rect = self.surf.get_rect(center=center)

    def click(self):
        print(self.text)


class MenuContext(GUIContext):
    def __init__(self, screen, model: GameModel, manager):
        super(MenuContext, self).__init__(screen, model, manager)
        self.newItem = MenuItem((200, 100), text="New Game", handler=self.newGameHandler)
        self.quitItem = MenuItem((200, 200), text="Quit Game", handler=self.quitHandler)
        self.nameItem = MenuItem((200, 300), text="Enter name", handler=self.nameHandler)
        self.saveItem = MenuItem((200, 400), text="Save Game", handler=self.saveHandler)
        self.loadItem = MenuItem((200, 500), text="Load Game", handler=self.loadHandler)

        all_sprites = pygame.sprite.Group()
        all_sprites.add(self.newItem)
        all_sprites.add(self.quitItem)
        all_sprites.add(self.nameItem)
        all_sprites.add(self.saveItem)
        all_sprites.add(self.loadItem)
        self.all_sprites = all_sprites

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
                for c in clicked_items:
                    returnCode = c.handler()
                    if returnCode != 0:
                        break

        self.screen.fill((135, 206, 250))

        for entity in self.all_sprites:
            self.screen.blit(entity.surf, entity.rect)

        return returnCode

    def quitHandler(self):
        print("Quitting...")
        pygame.event.post(pygame.event.Event(QUIT))
        return 0

    def newGameHandler(self):
        print("Loading...")
        self.model.load()
        return GUICode.LOADORBITVIEW

    def nameHandler(self):
        self.name = simpledialog.askstring(title = "Player Name", prompt="Enter name...")
        return 0

    def saveHandler(self):
        saveFile = filedialog.asksaveasfile(mode="wb", confirmoverwrite=True, defaultextension="sav", initialdir="D:\Applications\SpaceSim\Saves")
        if saveFile:
            self.model.saveModel(saveFile)
            saveFile.close()
            return GUICode.LOADORBITVIEW
        else:
            return 0

    def loadHandler(self):
        loadFile = filedialog.askopenfile(mode="rb")
        if loadFile:
            self.model.loadModel(loadFile)
            loadFile.close()
            return GUICode.LOADORBITVIEW
        else:
            return 0