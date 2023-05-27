import unittest

from views.colonyContext import ColonyContext
from views.guiContext import GUIContext

import pygame
import pygame_gui

class ModelMock:
    pass

class TestColonyContext(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.manager = pygame_gui.UIManager((1200, 800))
        screen = pygame.display.set_mode((1200, 800))

    def testColonyContext(self):
        self.assertTrue(ColonyContext)

    def testColonyContextConstructor(self):
        self.assertTrue(ColonyContext(ModelMock(), ModelMock(), None, None))

    def testColonyContextInheritance(self):
        cc = ColonyContext(ModelMock(), ModelMock(), None, None)
        self.assertTrue(issubclass(ColonyContext, GUIContext))
        self.assertTrue(isinstance(cc, GUIContext))
         