import pygame

from enum import Enum

class GUICode(Enum):
    LOADORBITVIEW = pygame.USEREVENT + 1
    LOADMENUVIEW = pygame.USEREVENT + 2
    LOADSURFACEVIEW = pygame.USEREVENT + 3
    LOADCOLONYVIEW = pygame.USEREVENT + 4
    LOADORBITVIEW_LAUNCH_PLAN = pygame.USEREVENT + 5
    LOADORBITVIEW_TARGET_RETURN = pygame.USEREVENT + 6
    LOADSURFACEVIEW_LANDING_PLAN = pygame.USEREVENT + 7
    LOADSURFACEVIEW_LAUNCH_RETURN = pygame.USEREVENT + 8
    LOADCOLONYVIEW_LAUNCH_RETURN = pygame.USEREVENT + 9

class GUIContext:
    def __init__(self, screen, model, manager):
        self.screen = screen
        self.model = model
        self.manager = manager

    def run(self):
        raise NotImplementedError