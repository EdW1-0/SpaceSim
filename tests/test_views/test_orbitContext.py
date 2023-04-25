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

    def testPlanetStatusPanelUpdate(self):
        psp = PlanetStatusPanel(pygame.Rect(800, 200, 400, 600), manager=self.manager)
        mp = ModelMock()
        mp.gravity = 10
        mn = ModelMock()
        mn.name = "Test Planet"
        mn.particles = []
        psp.set_node(mn)
        psp.set_planet(mp)
        psp.update()
        self.assertEqual(psp.planet_name_label.text, "Test Planet")

    def testPlanetStatusPanelEventHandling(self):
        psp = PlanetStatusPanel(pygame.Rect(800, 200, 400, 600), manager=self.manager)
        me = ModelMock()
        me.ui_element = None
        self.assertFalse(psp.handle_event(me))
        self.assertEqual(psp.upperAction, 0)
        me.ui_element = psp.surface_button
        self.assertTrue(psp.handle_event(me))
        self.assertEqual(psp.upperAction, 1)
        me.ui_element = psp.hide_button
        self.assertTrue(psp.container.visible)
        self.assertTrue(psp.handle_event(me))
        self.assertFalse(psp.container.visible)
        self.assertEqual(psp.upperAction, 0)

class TestOrbitStatusPanel(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.manager = pygame_gui.UIManager((1200, 800))
        screen = pygame.display.set_mode((1200, 800))

    def testOrbitStatusPanel(self):
        self.assertTrue(OrbitStatusPanel)

    def testOrbitStatusPanelConstructor(self):
        mn = ModelMock()
        self.assertTrue(OrbitStatusPanel(pygame.Rect(800, 200, 400, 600), manager=self.manager))

    def testOrbitStatusPanelUpdate(self):
        mn = ModelMock()
        mn.name = "Test Orbit"
        osp = OrbitStatusPanel(pygame.Rect(800, 200, 400, 600), manager=self.manager)
        osp.set_node(mn)
        osp.update()
        self.assertEqual(osp.orbit_name_label.text, "Test Orbit")

class TestLinkStatusPanel(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.manager = pygame_gui.UIManager((1200, 800))
        screen = pygame.display.set_mode((1200, 800))

    def testLinkStatusPanel(self):
        self.assertTrue(LinkStatusPanel)

    def testLinkStatusPanelConstructor(self):
        self.assertTrue(LinkStatusPanel(pygame.Rect(800, 200, 400, 600), manager=self.manager))

    def testLinkStatusPanelUpdate(self):
        lsp = LinkStatusPanel(pygame.Rect(800, 200, 400, 600), manager=self.manager)
        ml = ModelMock()
        ml.topNode = "ONE"
        ml.bottomNode = "TWO"
        lsp.set_link(ml)
        lsp.update()
        self.assertEqual(lsp.link_name_label.text, "ONE - TWO")

class TestShipStatusPanel(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.manager = pygame_gui.UIManager((1200, 800))
        self.orbitSim = OrbitSim(particlePath = "json/Particles.json")
        screen = pygame.display.set_mode((1200, 800))

    def testShipStatusPanel(self):
        self.assertTrue(ShipStatusPanel)

    def testShipStatusPanelConstructor(self):
        self.assertTrue(ShipStatusPanel(pygame.Rect(800, 200, 400, 600), manager=self.manager))

    def testShipStatusPanelUpdate(self):
        model = ModelMock()
        model.orbitSim = self.orbitSim
        ssp = ShipStatusPanel(pygame.Rect(800, 200, 400, 600), manager=self.manager, model = model)
        ship = ShipMock()
        ship.id = 0
        ship.velocity = 50
        ship.payload = ModelMock()
        ship.payload.name = "Test Ship"
        ssp.set_ship(ship)
        self.assertEqual(ssp.ship_location().id, "EAS")
        ssp.update()
        self.assertEqual(ssp.ship_name_label.text, "Test Ship")
        self.assertEqual(ssp.ship_text.html_text, "Delta V: 7m/s<br>Velocity: 50m/s<br>Location: Earth")

    def testShipStatusPanelHandleEvent(self):
        ssp = ShipStatusPanel(pygame.Rect(800, 200, 400, 600), manager=self.manager) 
        event = ModelMock()
        event.ui_element = None
        self.assertFalse(ssp.handle_event(event))
        self.assertEqual(ssp.upperAction, 0)
        event.ui_element = ssp.locationButton
        self.assertTrue(ssp.handle_event(event))
        self.assertEqual(ssp.upperAction, 1)
        event.ui_element = ssp.targetButton
        self.assertTrue(ssp.handle_event(event))
        self.assertEqual(ssp.upperAction, 2)
        event.ui_element = ssp.hide_button
        self.assertTrue(ssp.handle_event(event))
        self.assertEqual(ssp.container.visible, 0)
        self.assertEqual(ssp.upperAction, 0)

class TestTargetSettingPanel(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.manager = pygame_gui.UIManager((1200, 800))
        screen = pygame.display.set_mode((1200, 800))
        self.orbitSim = OrbitSim(particlePath = "json/Particles.json")

    def testTargetSettingPanel(self):
        self.assertTrue(TargetSettingPanel)

    def testTargetSettingPanelConstructor(self):
        self.assertTrue(TargetSettingPanel(pygame.Rect(800, 200, 400, 600), manager=self.manager))

    def testTargetSettingPanelUpdate(self):
        model = ModelMock()
        model.orbitSim = self.orbitSim
        tsp = TargetSettingPanel(pygame.Rect(800, 200, 400, 600), manager=self.manager, model=model)
        
        tsp.update()
        self.assertEqual(tsp.source_label.text, "")
        self.assertEqual(tsp.target_label.text, "")
        self.assertEqual(tsp.route_text.html_text, "")
        
        ms = ModelMock()
        ms.id = 0
        mso = ModelMock()
        mso.id = "EAS"
        mso.name = "Source"
        mto = ModelMock()
        mto.id = "MOS"
        mto.name = "Target"
        tsp.set_ship(ms)
        tsp.set_source(mso)
        tsp.set_target(mto)
        self.assertTrue(tsp.trajectory)
        self.assertEqual(tsp.source_label.text, "Source")
        self.assertEqual(tsp.target_label.text, "Target")
        self.assertEqual(tsp.route_text.html_text, "Delta V: 23m/s<br>Total time: 23<br>Total distance: 23")
        
        tsp.clear_state()
        self.assertEqual(tsp.source_label.text, "")
        self.assertEqual(tsp.target_label.text, "")
        self.assertEqual(tsp.route_text.html_text, "")

    def testTargetSettingPanelEventHandling(self):
        model = ModelMock()
        model.orbitSim = self.orbitSim
        tsp = TargetSettingPanel(pygame.Rect(800, 200, 400, 600), manager=self.manager, model=model)

        event = ModelMock()
        event.ui_element = None
        self.assertFalse(tsp.handle_event(event))
        self.assertEqual(tsp.upperAction, 0)
        event.ui_element = tsp.confirm_button
        self.assertTrue(tsp.handle_event(event))
        self.assertEqual(tsp.upperAction, 0)

        ms = ModelMock()
        ms.id = 0
        mso = ModelMock()
        mso.id = "EAS"
        mso.name = "Source"
        mto = ModelMock()
        mto.id = "MOS"
        mto.name = "Target"
        tsp.set_ship(ms)
        tsp.set_source(mso)
        tsp.set_target(mto)

        self.assertTrue(tsp.handle_event(event))
        self.assertEqual(tsp.trajectory.state, TrajectoryState.PENDING)
        self.assertEqual(tsp.upperAction, 1)
        self.assertEqual(tsp.container.visible, 0)


class TestOrbitContext(unittest.TestCase):
    def testOrbitContext(self):
        self.assertTrue(OrbitContext)

    