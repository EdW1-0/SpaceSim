import unittest

from views.colonyContext import ColonyContext
from views.guiContext import GUIContext

import pygame
import pygame_gui

class ModelMock:
    orbitSim = None

class TestColonyContext(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.manager = pygame_gui.UIManager((1200, 800))
        screen = pygame.display.set_mode((1200, 800))
        self.mm = ModelMock()
        self.mm.timingMaster = ModelMock()

        self.cm = ModelMock()
        self.cm.vehicles = {}
        self.cm.ships = {}

    def testColonyContext(self):
        self.assertTrue(ColonyContext)

    def testColonyContextConstructor(self):
        self.assertTrue(ColonyContext(ModelMock(), self.mm, self.manager, self.cm))

    def testColonyContextInheritance(self):
        cc = ColonyContext(ModelMock(), self.mm, self.manager, self.cm)
        self.assertTrue(issubclass(ColonyContext, GUIContext))
        self.assertTrue(isinstance(cc, GUIContext))
         