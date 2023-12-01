import pygame

from enum import Enum


class GUICode(Enum):
    LOADORBITVIEW = pygame.USEREVENT + 1
    LOADMENUVIEW = pygame.USEREVENT + 2
    LOADTECHVIEW = pygame.USEREVENT + 3
    LOADSURFACEVIEW = pygame.USEREVENT + 4
    LOADCOLONYVIEW = pygame.USEREVENT + 5
    LOADORBITVIEW_LAUNCH_PLAN = pygame.USEREVENT + 6
    LOADORBITVIEW_TARGET_RETURN = pygame.USEREVENT + 7
    LOADSURFACEVIEW_LANDING_PLAN = pygame.USEREVENT + 8
    LOADSURFACEVIEW_LAUNCH_RETURN = pygame.USEREVENT + 9
    LOADCOLONYVIEW_LAUNCH_RETURN = pygame.USEREVENT + 10
    LOADORBITVIEW_LAUNCH_LAND_RETURN = pygame.USEREVENT + 11


class GUIContext:
    def __init__(self, screen, model, manager):
        self.screen = screen
        self.model = model
        self.manager = manager

    def run(self):
        raise NotImplementedError
