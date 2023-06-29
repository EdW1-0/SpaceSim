import pygame

from enum import Enum

class GUICode(Enum):
    LOADORBITVIEW = pygame.USEREVENT + 1
    LOADMENUVIEW = pygame.USEREVENT + 2
    LOADSURFACEVIEW = pygame.USEREVENT + 3
    LOADCOLONYVIEW = pygame.USEREVENT + 4

class GUIContext:
    def __init__(self, screen, model, manager):
        self.screen = screen
        self.model = model
        self.manager = manager

    def run(self):
        raise NotImplementedError