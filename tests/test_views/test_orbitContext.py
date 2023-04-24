from views.orbitContext import OrbitContext, PlanetStatusPanel
from views.guiContext import GUIContext

import unittest
from tests.test_views.test_guiContext import ScreenMock, ModelMock

import pygame
import pygame_gui



class ModelMock:
    pass

class TestPlanetStatusPanel(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.manager = pygame_gui.UIManager((1200, 800))
        screen = pygame.display.set_mode((1200, 800))

    def testPlanetStatusPanel(self):
        self.assertTrue(PlanetStatusPanel)

    def testPlanetStatusPanelConstructor(self):
        self.assertTrue(PlanetStatusPanel(pygame.Rect(800, 200, 400, 600), manager=self.manager))
        self.assertTrue(PlanetStatusPanel(pygame.Rect(800, 200, 400, 600), manager=self.manager, model=ModelMock()))

    def testPlanetStatusPanelAttributes(self):
        psp = PlanetStatusPanel(pygame.Rect(800, 200, 400, 600), manager=self.manager)
        self.assertTrue(hasattr(psp, "model"))
        self.assertTrue(hasattr(psp, "planet_name_label"))
        self.assertTrue(hasattr(psp, "planet_image"))
        self.assertTrue(hasattr(psp, "planet_text"))
        self.assertTrue(hasattr(psp, "atmosphere_button"))
        self.assertTrue(hasattr(psp, "surface_button"))
        self.assertTrue(hasattr(psp, "station_list"))
        



class TestOrbitContext(unittest.TestCase):
    def testOrbitContext(self):
        self.assertTrue(OrbitContext)

    