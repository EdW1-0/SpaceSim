import unittest

from views.colonyContext import ColonyContext
from views.guiContext import GUIContext

from gameModel import GameModel

import pygame
import pygame_gui

from tests.test_views.test_guiContext import isLocal


class ColonySimMock:
    _resources = None
    _reactions = None

    def buildingClassesForColony(self, c):
        return None


class ModelMock:
    id = None
    orbitSim = None
    buildings = None
    productionOrders = None
    colonySim = ColonySimMock()

@unittest.skipUnless(isLocal(), "requires Windows")
class TestColonyContext(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.manager = pygame_gui.UIManager((1200, 800))
        pygame.display.set_mode((1200, 800))
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

@unittest.skipUnless(isLocal(), "requires Windows")
class TestColonyContextTabPanel(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.manager = pygame_gui.UIManager((1200, 800))
        pygame.display.set_mode((1200, 800))

        self.model = GameModel()
        self.model.load()

        self.cm = ModelMock()
        self.cm.vehicles = {}
        self.cm.ships = {}

        self.cc = ColonyContext(ModelMock(), self.model, self.manager, self.model.colonySim.colonyById(0))

    def testColonyContextTabBuildings(self):
        event = ModelMock()
        event.ui_element = self.cc.tab_panel.buildings_button

        self.assertEqual(self.cc.handleGuiButton(event), 0)
        self.assertEqual(self.cc.active_panel, self.cc.building_panel)

        event.ui_element = self.cc.tab_panel.construction_button

        self.assertEqual(self.cc.handleGuiButton(event), 0)
        self.assertEqual(self.cc.active_panel, self.cc.construction_panel)

        event.ui_element = self.cc.tab_panel.resource_button

        self.assertEqual(self.cc.handleGuiButton(event), 0)
        self.assertEqual(self.cc.active_panel, self.cc.resource_panel)

        event.ui_element = self.cc.tab_panel.production_button

        self.assertEqual(self.cc.handleGuiButton(event), 0)
        self.assertEqual(self.cc.active_panel, self.cc.production_panel)

        event.ui_element = self.cc.tab_panel.vehicles_button

        self.assertEqual(self.cc.handleGuiButton(event), 0)
        self.assertEqual(self.cc.active_panel, self.cc.vehicle_panel)

        event.ui_element = self.cc.tab_panel.ships_button

        self.assertEqual(self.cc.handleGuiButton(event), 0)
        self.assertEqual(self.cc.active_panel, self.cc.ship_panel)



