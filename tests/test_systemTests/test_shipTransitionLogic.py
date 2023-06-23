import unittest
import pygame

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    MOUSEBUTTONUP,
    QUIT,
)

from pygame.event import Event

from pygame_gui  import (
    UI_BUTTON_PRESSED,
    UI_SELECTION_LIST_NEW_SELECTION
)

import spacesim

from views.menuContext import MenuContext
from views.orbitContext import OrbitContext, OrbitNodeView, OrbitLinkView, OCMode
from views.surfaceContext import SurfaceContext, SCMode
from views.colonyContext import ColonyContext
from planetsim.surfaceBase import SurfaceBase

class SystemTestShipLandingLogic(unittest.TestCase):
    def testShipLandingLogicRunner(self):
        self.runCount = 0
        self.testPassed = False
        spacesim.main(testingCallback=self.shipLandingLogicCallback)

    def shipLandingLogicCallback(self, model, guiContext):
        if isinstance(guiContext, MenuContext):
            pos = guiContext.loadItem.rect.center
            pygame.mouse.set_pos(pos)
            pygame.event.post(Event(MOUSEBUTTONUP))
            self.assertEqual(self.runCount, 0)
        elif isinstance(guiContext, OrbitContext):
            self.assertGreaterEqual(self.runCount, 1)
            mercury = None
            mercuryOrbit = None
            for s in guiContext.all_sprites:
                if not isinstance(s, OrbitNodeView):
                    continue
                if s.node.id == "MEO":
                    mercuryOrbit = s
                elif s.node.id == "MES":
                    mercury = s
            
            if self.runCount == 1:
                self.assertTrue(isinstance(guiContext, OrbitContext))
                guiContext.resolveNodeClick(mercuryOrbit)
            elif self.runCount == 2:
                self.assertEqual(guiContext.active_summary, guiContext.orbit_summary)
                event = Event(UI_SELECTION_LIST_NEW_SELECTION)
                event.ui_element = guiContext.orbit_summary.station_list 
                event.text= "ISS Meghalaya"
                pygame.event.post(event)
            elif self.runCount == 3:
                self.assertEqual(guiContext.active_summary, guiContext.ship_summary)
                pygame.event.post(Event(UI_BUTTON_PRESSED, ui_element = guiContext.ship_summary.targetButton))
            elif self.runCount == 4:
                self.assertTrue(guiContext.target_panel.container.visible)
                guiContext.resolveNodeClick(mercury)
            elif self.runCount == 5:
                pygame.event.post(Event(UI_BUTTON_PRESSED, ui_element = guiContext.target_panel.surface_button))
            elif self.runCount == 8:
                self.assertTrue(guiContext.target_panel.trajectory)
                self.assertEqual(guiContext.target_panel.target.id, "MES")
                pygame.event.post(Event(UI_BUTTON_PRESSED, ui_element = guiContext.target_panel.confirm_button))
            elif self.runCount == 9:
                pygame.event.post(Event(UI_BUTTON_PRESSED, ui_element = guiContext.timing_panel.start_button))
            elif self.runCount == 50:
                pygame.event.post(Event(UI_BUTTON_PRESSED, ui_element = guiContext.timing_panel.stop_button))
            elif self.runCount == 51:
                surface = model.planetSim.planetById("MERCURY").surface
                self.assertEqual(surface.points[3].name, "ISS Meghalaya")
                self.testPassed = True

        elif isinstance(guiContext, SurfaceContext):
            if self.runCount == 6:
                self.assertTrue(guiContext, SurfaceContext)
                self.assertEqual(guiContext.targetMode, SCMode.Landing)
                guiContext.hitTestRegion((400, 400))
            elif self.runCount == 7:
                self.assertTrue(guiContext.target_panel.target)
                pygame.event.post(Event(UI_BUTTON_PRESSED, ui_element = guiContext.target_panel.confirm_button))




        if self.runCount == 60:
            self.assertTrue(self.testPassed)
            pygame.event.post(Event(QUIT))
        self.runCount += 1
        return
    
class SystemTestColonyShipLaunch(unittest.TestCase):
    def testColonyShipLaunch(self):
        self.runCount = 0
        self.testPassed = False
        spacesim.main(testingCallback = self.colonyShipLaunchCallback)

    def colonyShipLaunchCallback(self, model, guiContext):
        if isinstance(guiContext, MenuContext):
            pos = guiContext.loadItem.rect.center
            pygame.mouse.set_pos(pos)
            pygame.event.post(Event(MOUSEBUTTONUP))
            self.assertEqual(self.runCount, 0)

        elif isinstance(guiContext, OrbitContext):
            mercury = None
            for s in guiContext.all_sprites:
                if not isinstance(s, OrbitNodeView):
                    continue
                if s.node.id == "MES":
                    mercury = s

            if self.runCount == 1:
                self.assertTrue(isinstance(guiContext, OrbitContext))
                guiContext.resolveNodeClick(mercury)
            elif self.runCount == 2:
                self.assertEqual(guiContext.active_summary, guiContext.planet_summary)
                event = Event(UI_BUTTON_PRESSED, ui_element = guiContext.planet_summary.surface_button)
                pygame.event.post(event)

            elif self.runCount == 8:
                self.assertEqual(guiContext.target_mode, OCMode.LaunchPlan)
                mercuryTransfer = None
                for s in guiContext.all_sprites:
                    if not isinstance(s, OrbitNodeView):
                        continue
                    if s.node.id == "MET":
                        mercuryTransfer = s
                guiContext.resolveNodeClick(mercuryTransfer)

            elif self.runCount == 9:
                self.assertTrue(guiContext.target_panel.container.visible)
                pygame.event.post(Event(UI_BUTTON_PRESSED, ui_element = guiContext.target_panel.confirm_button))


        elif isinstance(guiContext, SurfaceContext):
            base = None
            for s in guiContext.all_sprites:
                if isinstance(s.surfaceObject, SurfaceBase):
                    base = s 
            
            if self.runCount == 3:
                self.assertTrue(guiContext.handleClickedObject(base))
                self.assertEqual(guiContext.active_panel, guiContext.vehicle_panel)
            elif self.runCount == 4:
                event = pygame.event.Event(UI_BUTTON_PRESSED, ui_element = guiContext.vehicle_panel.colony_button)
                pygame.event.post(event)

        elif isinstance(guiContext, ColonyContext):
            if self.runCount == 5:
                pygame.event.post(Event(UI_BUTTON_PRESSED, ui_element = guiContext.tab_panel.ships_button))
            elif self.runCount == 6:
                self.assertEqual(guiContext.active_panel, guiContext.ship_panel)
                event = Event(UI_SELECTION_LIST_NEW_SELECTION)
                event.ui_element = guiContext.ship_panel.ships_list 
                event.text= "MSS Viking"
                pygame.event.post(event)
            elif self.runCount == 7:
                self.assertEqual(guiContext.detail_panel, guiContext.ship_detail_panel)
                pygame.event.post(Event(UI_BUTTON_PRESSED, ui_element = guiContext.ship_detail_panel.target_button))

            elif self.runCount == 10:
                self.assertEqual(guiContext.detail_panel, guiContext.ship_detail_panel)
                pygame.event.post(Event(UI_BUTTON_PRESSED, ui_element = guiContext.ship_detail_panel.launch_button))
            elif self.runCount == 11:
                pygame.event.post(Event(UI_BUTTON_PRESSED, ui_element = guiContext.timing_panel.start_button))
            elif self.runCount == 50:
                pygame.event.post(Event(UI_BUTTON_PRESSED, ui_element = guiContext.timing_panel.stop_button))
            elif self.runCount == 51:
                mercuryTransfer = model.orbitSim.nodeById("MET")
                self.assertGreater(len(mercuryTransfer.particles), 0)
                ship = mercuryTransfer.particles.pop()
                self.assertEqual(ship, 4)
                shipObj = model.orbitSim.particleById(ship)
                self.assertEqual(shipObj.payload.name, "MSS Viking")
                self.testPassed = True





        if self.runCount == 60:
            self.assertTrue(self.testPassed)
            pygame.event.post(Event(QUIT))
        self.runCount += 1
        return
    
class SystemTestContextStack(unittest.TestCase):
    def testContextStack(self):
        self.runCount = 0
        self.testPassed = False
        spacesim.main(testingCallback=self.contextStackCallback)

    def contextStackCallback(self, model, guiContext):
        if isinstance(guiContext, MenuContext):
            pos = guiContext.loadItem.rect.center
            pygame.mouse.set_pos(pos)
            pygame.event.post(Event(MOUSEBUTTONUP))
            self.assertEqual(self.runCount, 0)

        elif isinstance(guiContext, OrbitContext):
            mercury = None
            for s in guiContext.all_sprites:
                if not isinstance(s, OrbitNodeView):
                    continue
                if s.node.id == "MES":
                    mercury = s

            if self.runCount == 1:
                self.assertTrue(isinstance(guiContext, OrbitContext))
                guiContext.resolveNodeClick(mercury)
            elif self.runCount == 2:
                self.assertEqual(guiContext.active_summary, guiContext.planet_summary)
                event = Event(UI_BUTTON_PRESSED, ui_element = guiContext.planet_summary.surface_button)
                pygame.event.post(event)
            elif self.runCount == 7:
                self.testPassed = True

        elif isinstance(guiContext, SurfaceContext):
            base = None
            for s in guiContext.all_sprites:
                if isinstance(s.surfaceObject, SurfaceBase):
                    base = s 
            
            if self.runCount == 3:
                self.assertTrue(guiContext.handleClickedObject(base))
                self.assertEqual(guiContext.active_panel, guiContext.vehicle_panel)
            elif self.runCount == 4:
                event = pygame.event.Event(UI_BUTTON_PRESSED, ui_element = guiContext.vehicle_panel.colony_button)
                pygame.event.post(event)
            elif self.runCount == 6:
                pygame.event.post(Event(UI_BUTTON_PRESSED, ui_element = guiContext.settings_button))

        elif isinstance(guiContext, ColonyContext):
            self.assertGreater(self.runCount, 4)
            pygame.event.post(Event(UI_BUTTON_PRESSED, ui_element = guiContext.settings_button))

        
        if self.runCount == 30:
            self.assertTrue(self.testPassed)
            pygame.event.post(Event(QUIT))
        self.runCount += 1
        return