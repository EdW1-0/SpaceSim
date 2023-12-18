import unittest
from unittest.mock import MagicMock

from views.colonyContext import ColonyContext
from views.guiContext import GUIContext, GUICode

from gameModel import GameModel

from orbitsim.orbitTrajectory import TrajectoryState

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
class TestColonyContextHandleGUIButton(unittest.TestCase):
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

    def testColonyContextSettingsButton(self):
        event = ModelMock()
        event.ui_element = self.cc.settings_button

        self.assertEqual(self.cc.handleGuiButton(event), GUICode.LOADSURFACEVIEW)
        self.assertEqual(self.cc.upperContext["planet"], "MERCURY")

    def testColontContextTimingPanel(self):
        event = ModelMock()
        event.ui_element = self.cc.timing_panel.stop_button

        self.assertEqual(self.cc.handleGuiButton(event), 0)


    def testColonyContextTabPanel(self):
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

    def testColonyContextShipPanel(self):
        event = ModelMock()
        event.ui_element = self.cc.ship_panel.hide_button
        self.cc.active_panel = self.cc.ship_panel
        self.cc.active_panel.show()
        self.cc.detail_panel = self.cc.ship_detail_panel

        self.assertTrue(self.cc.active_panel.container.visible)
        self.assertEqual(self.cc.handleGuiButton(event), 0)
        self.assertFalse(self.cc.active_panel.container.visible)

        self.cc.active_panel.show()

        self.cc.detail_panel = None
        event.ui_element = self.cc.ship_panel.target_button

        self.assertEqual(self.cc.handleGuiButton(event), 0)
        self.assertEqual(self.cc.detail_panel, self.cc.ship_detail_panel)
        self.assertTrue(self.cc.ship_detail_panel.container.visible)

        event.ui_element = self.cc.ship_panel.loading_button

        self.assertEqual(self.cc.handleGuiButton(event), 0)
        self.assertEqual(self.cc.detail_panel, self.cc.ship_loading_panel)
        self.assertTrue(self.cc.ship_loading_panel.container.visible)

    def testColonyContextVehiclePanel(self):
        event = ModelMock()
        event.ui_element = self.cc.vehicle_panel.target_button
        self.cc.active_panel = self.cc.vehicle_panel
        self.cc.active_panel.show()

        self.assertEqual(self.cc.handleGuiButton(event), 0)
        self.assertEqual(self.cc.detail_panel, self.cc.vehicle_detail_panel)
        self.assertTrue(self.cc.detail_panel.container.visible)

        event.ui_element = self.cc.vehicle_panel.loading_button

        self.assertEqual(self.cc.handleGuiButton(event), 0)
        self.assertEqual(self.cc.detail_panel, self.cc.vehicle_loading_panel)
        self.assertTrue(self.cc.vehicle_loading_panel.container.visible)

    def testColonyContextShipDetailPanel(self):
        event = ModelMock()
        event.ui_element = self.cc.ship_detail_panel.target_button
        self.cc.detail_panel = self.cc.ship_detail_panel
        ship = ModelMock()
        self.cc.ship_detail_panel.ship = ship

        self.assertEqual(self.cc.handleGuiButton(event), GUICode.LOADORBITVIEW_LAUNCH_PLAN)
        self.assertEqual(self.cc.info.ship, ship)
        self.assertEqual(self.cc.info.start, self.cc.colony)

        event.ui_element = self.cc.ship_detail_panel.launch_button
        mockTrajectory = ModelMock()
        self.cc.ship_detail_panel.trajectory = MagicMock(return_value = mockTrajectory)

        self.assertEqual(self.cc.handleGuiButton(event), 0)
        self.assertEqual(mockTrajectory.state, TrajectoryState.PENDING)

        event.ui_element = self.cc.ship_detail_panel.hide_button

        self.assertEqual(self.cc.handleGuiButton(event), 0)
        self.assertFalse(self.cc.ship_detail_panel.container.visible)

    def testColonyContextVehicleDetailPanel(self):
        event = ModelMock()
        event.ui_element = self.cc.vehicle_detail_panel.embark_button
        self.cc.detail_panel = self.cc.vehicle_detail_panel
        self.cc.active_panel = self.cc.vehicle_panel
        vehicle = self.cc.colony.vehicleById(1)
        self.cc.vehicle_detail_panel.vehicle = vehicle

        self.assertEqual(self.cc.handleGuiButton(event), 0)
        self.assertIsNone(self.cc.detail_panel)
        self.assertEqual(len(self.cc.colony.vehicles), 0)

@unittest.skipUnless(isLocal(), "requires Windows")
class TestColonyContextHandleListSelection(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.manager = pygame_gui.UIManager((1200, 800))
        pygame.display.set_mode((1200, 800))

        self.model = GameModel()
        self.model.load()

        self.model.playerTech.setActiveTech(1)
        self.model.playerTech._completeTech()
        self.model.playerTech.setActiveTech(2)
        self.model.playerTech._completeTech()
        self.model.playerTech.setActiveTech(3)
        self.model.playerTech._completeTech()

        self.cm = ModelMock()
        self.cm.vehicles = {}
        self.cm.ships = {}

        self.cc = ColonyContext(ModelMock(), self.model, self.manager, self.model.colonySim.colonyById(0))

    def testColonyContextPopulateDetailPanel(self):
        detail_panel = ModelMock()
        detail_panel.show = MagicMock()
        detail_panel.update = MagicMock()
        detail_panel.setter = MagicMock()

        source_list = [1,2,3,4,5,6,7]

        self.cc.populateDetailPanel(
            5, 
            source_list, 
            detail_panel, 
            detail_panel.setter, 
            lambda item, key: item == key
            )
        self.assertEqual(self.cc.detail_panel, detail_panel)
        detail_panel.show.assert_called()
        detail_panel.update.assert_called()
        detail_panel.setter.assert_called_with(5)

    def testColonyContextListSelection(self):
        event = ModelMock()
        event.ui_element = self.cc.vehicle_panel.item_list
        vehicle = next(iter(self.cc.colony.vehicles.values()))
        event.text = vehicle.name

        self.assertEqual(self.cc.handleListSelection(event), 0)
        self.assertEqual(self.cc.vehicle_panel.ship, vehicle)
        self.assertEqual(self.cc.detail_panel, self.cc.vehicle_detail_panel)
        self.assertEqual(self.cc.vehicle_detail_panel.vehicle, vehicle)

        event.ui_element = self.cc.ship_panel.item_list
        ship = next(iter(self.cc.colony.ships.values()))
        event.text = ship.name

        self.assertEqual(self.cc.handleListSelection(event), 0)
        self.assertEqual(self.cc.ship_panel.ship, ship)
        self.assertEqual(self.cc.detail_panel, self.cc.ship_detail_panel)
        self.assertEqual(self.cc.ship_detail_panel.ship, ship)

        event.text = "Energy"
        event.ui_element = self.cc.vehicle_loading_panel.item_list
        self.cc.detail_panel = self.cc.vehicle_loading_panel
        self.cc.vehicle_loading_panel.setShip(vehicle)

        self.assertEqual(self.cc.handleListSelection(event), 0)
        self.assertEqual(self.cc.vehicle_loading_panel.resource.name, event.text)

        event.ui_element = self.cc.ship_loading_panel.item_list
        self.cc.detail_panel = self.cc.ship_loading_panel
        self.cc.ship_loading_panel.setShip(ship)

        self.assertEqual(self.cc.handleListSelection(event), 0)
        self.assertEqual(self.cc.ship_loading_panel.resource.name, event.text)
        
        event.ui_element = self.cc.building_panel.item_list
        building = next(iter(self.cc.colony.buildings.values()))
        event.text = building.buildingClass.name + " " + str(building.id)

        self.assertEqual(self.cc.handleListSelection(event), 0)
        self.assertEqual(self.cc.detail_panel, self.cc.building_detail_panel)
        self.assertEqual(self.cc.building_detail_panel.building, building)



        event.ui_element = self.cc.construction_panel.item_list
        buildingClass = next(iter(self.cc.model.colonySim.buildingClassesForColony(self.cc.colony.id).values()))
        event.text = buildingClass.name

        self.assertEqual(self.cc.handleListSelection(event), 0)
        self.assertEqual(self.cc.detail_panel, self.cc.construction_detail_panel)
        self.assertEqual(self.cc.construction_detail_panel.buildingClass, buildingClass)

        event.ui_element = self.cc.production_panel.item_list
        po = next(iter(self.cc.colony.productionOrders.values()))
        self.cc.production_panel.update()
        self.cc.production_panel.item_list.item_list[0]['selected'] = True

        self.assertEqual(self.cc.handleListSelection(event), 0)
        (text, id) = self.cc.production_panel.item_list.get_single_selection()
        self.assertEqual(self.cc.production_panel.productionOrder.id, int(id))

        event.ui_element = self.cc.production_detail_panel.item_list
        reaction = next(iter(self.cc.model.colonySim._reactions.values()))
        event.text = reaction.name

        self.assertEqual(self.cc.handleListSelection(event), 0)
        self.assertEqual(self.cc.production_detail_panel.reaction, reaction)

        event.ui_element = self.cc.resource_panel.item_list
        resource = next(iter(self.model.colonySim._resources.values()))
        event.text = resource.name

        self.assertEqual(self.cc.handleListSelection(event), 0)
        self.assertEqual(self.cc.resource_detail_panel, self.cc.detail_panel)
        self.assertEqual(self.cc.resource_detail_panel.resource, resource)







