from views.orbitContext import OrbitContext, PlanetStatusPanel, OrbitStatusPanel, LinkStatusPanel, ShipStatusPanel, TargetSettingPanel
from views.guiContext import GUIContext

import unittest
from tests.test_views.test_guiContext import ScreenMock, ModelMock
from orbitsim.orbitSim import OrbitSim, TrajectoryState

import pygame
import pygame_gui



class ModelMock:
    pass

class ShipMock:
    def deltaV(self):
        return 7



class TestOrbitContext(unittest.TestCase):
    def testOrbitContext(self):
        self.assertTrue(OrbitContext)

    def setUp(self):
        self.mm = ModelMock()
        tm = ModelMock()
        os = OrbitSim()
        self.mm.timingMaster = tm
        self.mm.orbitSim = os
        pygame.init()
        self.manager = pygame_gui.UIManager((1200, 800))
        screen = pygame.display.set_mode((1200, 800))

    def testOrbitContextConstructor(self):
        self.assertTrue(OrbitContext(None, self.mm, self.manager))

    