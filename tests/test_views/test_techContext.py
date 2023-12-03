import unittest

from views.techContext import TechContext

from views.guiContext import GUIContext

from gameModel import GameModel

import pygame
import pygame_gui

from tests.test_views.test_guiContext import ModelMock, isLocal



@unittest.skipUnless(isLocal(), "requires Windows")
class TestTechContext(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.manager = pygame_gui.UIManager((1200, 800))
        pygame.display.set_mode((1200, 800))

        self.gm = GameModel()
        self.gm.load()

    def testTechContext(self):
        self.assertTrue(TechContext)

    def testTechContextClassHierarchy(self):
        self.assertTrue(TechContext(None, self.gm, None))
        self.assertTrue(issubclass(TechContext, GUIContext))