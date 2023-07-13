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

from pygame.event import Event, post

from pygame_gui  import (
    UI_BUTTON_PRESSED,
    UI_SELECTION_LIST_NEW_SELECTION
)

import spacesim

from views.menuContext import MenuContext
from views.orbitContext import OrbitContext, OrbitNodeView, OrbitLinkView, OCMode
from views.surfaceContext import SurfaceContext, SCMode, SurfaceObjectSprite
from views.colonyContext import ColonyContext
from planetsim.surfaceBase import SurfaceBase
from planetsim.surfaceObject import SurfaceObject
from colonysim.ship import Ship

class SystemTestMacros:
    def goToColony(self, terminator, guiContext, model):
        if self.runCount >= terminator:
            return True
        if isinstance(guiContext, MenuContext):
            pos = guiContext.loadItem.rect.center
            pygame.mouse.set_pos(pos)
            post(Event(MOUSEBUTTONUP))
        elif isinstance(guiContext, OrbitContext):
            mercury = None
            for s in guiContext.all_sprites:
                if not isinstance(s, OrbitNodeView):
                    continue
                if s.node.id == "MES":
                    mercury = s

            if self.runCount == 1:
                guiContext.resolveNodeClick(mercury)
            elif self.runCount == 2:
                event = Event(UI_BUTTON_PRESSED, ui_element = guiContext.planet_summary.surface_button)
                post(event)

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
                post(event)
                return True
            
        return False



class SystemTestShipLandingLogic(unittest.TestCase):
    def testShipLandingLogicRunner(self):
        self.runCount = 0
        self.testPassed = False
        spacesim.main(testingCallback=self.shipLandingLogicCallback)

    def shipLandingLogicCallback(self, model, guiContext):
        if isinstance(guiContext, MenuContext):
            pos = guiContext.loadItem.rect.center
            pygame.mouse.set_pos(pos)
            post(Event(MOUSEBUTTONUP))
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
                post(event)
            elif self.runCount == 3:
                self.assertEqual(guiContext.active_summary, guiContext.ship_summary)
                post(Event(UI_BUTTON_PRESSED, ui_element = guiContext.ship_summary.targetButton))
            elif self.runCount == 4:
                self.assertTrue(guiContext.target_panel.container.visible)
                guiContext.resolveNodeClick(mercury)
            elif self.runCount == 5:
                post(Event(UI_BUTTON_PRESSED, ui_element = guiContext.target_panel.surface_button))
            elif self.runCount == 8:
                self.assertTrue(guiContext.target_panel.trajectory)
                self.assertEqual(guiContext.target_panel.target.id, "MES")
                post(Event(UI_BUTTON_PRESSED, ui_element = guiContext.target_panel.confirm_button))
            elif self.runCount == 9:
                post(Event(UI_BUTTON_PRESSED, ui_element = guiContext.timing_panel.start_button))
            elif self.runCount == 50:
                post(Event(UI_BUTTON_PRESSED, ui_element = guiContext.timing_panel.stop_button))
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
                post(Event(UI_BUTTON_PRESSED, ui_element = guiContext.target_panel.confirm_button))




        if self.runCount == 60:
            self.assertTrue(self.testPassed)
            post(Event(QUIT))
        self.runCount += 1
        return
    
class SystemTestSurfaceLaunch(SystemTestShipLandingLogic, SystemTestMacros):
    def testSurfaceLaunch(self):
        self.runCount = 0
        self.lowerTestPassed = False
        spacesim.main(testingCallback= self.surfaceLaunchCallback)

    def surfaceLaunchCallback(self, model, guiContext):
        if self.runCount < 52:
            self.shipLandingLogicCallback(model, guiContext)
            return
        else:
            if isinstance(guiContext, OrbitContext):
                mercury = None
                for s in guiContext.all_sprites:
                    if not isinstance(s, OrbitNodeView):
                        continue
                    if s.node.id == "MES":
                        mercury = s

                if self.runCount == 52:
                    self.assertTrue(isinstance(guiContext, OrbitContext))
                    guiContext.resolveNodeClick(mercury)
                elif self.runCount == 53:
                    post(Event(UI_BUTTON_PRESSED, ui_element=guiContext.planet_summary.surface_button))
                elif self.runCount == 56:
                    self.assertEqual(guiContext.target_mode, OCMode.LaunchPlan)
                    mercuryOrbit = None
                    for s in guiContext.all_sprites:
                        if not isinstance(s, OrbitNodeView):
                            continue
                        if s.node.id == "MEO":
                            mercuryOrbit = s
                    guiContext.resolveNodeClick(mercuryOrbit)
                elif self.runCount == 57:
                    post(Event(UI_BUTTON_PRESSED, ui_element =guiContext.target_panel.confirm_button))

            elif isinstance(guiContext, SurfaceContext):
                if self.runCount == 54:
                    ship = None
                    for s in guiContext.all_sprites:
                        if isinstance(s, SurfaceObjectSprite):
                            if isinstance(s.surfaceObject.content, Ship):
                                ship = s
                    guiContext.handleClickedObject(ship)
                elif self.runCount == 55:
                    post(Event(UI_BUTTON_PRESSED, ui_element = guiContext.vehicle_panel.target_button))
                elif self.runCount == 58:
                    self.assertTrue(guiContext.ship_panel.container.visible)
                    post(Event(UI_BUTTON_PRESSED, ui_element = guiContext.ship_panel.launch_button))
                elif self.runCount == 59:
                    post(Event(UI_BUTTON_PRESSED, ui_element = guiContext.timing_panel.start_button))
                elif self.runCount == 70:
                    post(Event(UI_BUTTON_PRESSED, ui_element = guiContext.timing_panel.stop_button))
                elif self.runCount == 71:
                    self.assertGreater(len(model.orbitSim.nodeById("MEO").particles), 0)
                    particleId = model.orbitSim.nodeById("MEO").particles.pop()
                    particle = model.orbitSim.particleById(particleId)
                    
                    self.assertEqual(particle.payload.name, "ISS Meghalaya")
                    surfaceObj = model.planetSim.planetById("MERCURY").surface.objectForContent(particle.payload)
                    self.assertIsNone(surfaceObj)

                    self.lowerTestPassed = True

                



        if self.runCount == 80:
            self.assertTrue(self.lowerTestPassed)
            post(Event(QUIT))
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
            post(Event(MOUSEBUTTONUP))
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
                post(event)

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
                post(Event(UI_BUTTON_PRESSED, ui_element = guiContext.target_panel.confirm_button))


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
                post(event)

        elif isinstance(guiContext, ColonyContext):
            if self.runCount == 5:
                post(Event(UI_BUTTON_PRESSED, ui_element = guiContext.tab_panel.ships_button))
            elif self.runCount == 6:
                self.assertEqual(guiContext.active_panel, guiContext.ship_panel)
                event = Event(UI_SELECTION_LIST_NEW_SELECTION)
                event.ui_element = guiContext.ship_panel.item_list  
                event.text= "MSS Viking"
                post(event)
            elif self.runCount == 7:
                self.assertEqual(guiContext.detail_panel, guiContext.ship_detail_panel)
                post(Event(UI_BUTTON_PRESSED, ui_element = guiContext.ship_detail_panel.target_button))

            elif self.runCount == 10:
                self.assertEqual(guiContext.detail_panel, guiContext.ship_detail_panel)
                post(Event(UI_BUTTON_PRESSED, ui_element = guiContext.ship_detail_panel.launch_button))
            elif self.runCount == 11:
                post(Event(UI_BUTTON_PRESSED, ui_element = guiContext.timing_panel.start_button))
            elif self.runCount == 50:
                post(Event(UI_BUTTON_PRESSED, ui_element = guiContext.timing_panel.stop_button))
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
            post(Event(QUIT))
        self.runCount += 1
        return
    
class SystemTestColonySurfaceLaunchLand(SystemTestColonyShipLaunch):
    def testColonyLaunchLand(self):
        self.runCount = 0
        self.outerTestPassed = False
        spacesim.main(testingCallback=self.colonyLaunchLandCallback)

    def colonyLaunchLandCallback(self, model, guiContext):
        if self.runCount < 8:
            self.colonyShipLaunchCallback(model, guiContext)
            return
        
        if self.runCount == 8:
            moon = None
            for s in guiContext.all_sprites:
                if not isinstance(s, OrbitNodeView):
                    continue
                if s.node.id == "MOS":
                    moon = s

            self.assertTrue(isinstance(guiContext, OrbitContext))
            guiContext.resolveNodeClick(moon)
        if self.runCount == 9:
            self.assertTrue(isinstance(guiContext, OrbitContext))
            self.assertEqual(guiContext.target_mode, OCMode.LaunchPlan)
            post(Event(UI_BUTTON_PRESSED, ui_element = guiContext.target_panel.surface_button))
        elif self.runCount == 10:
            self.assertTrue(isinstance(guiContext, SurfaceContext))
            self.assertEqual(guiContext.targetMode, SCMode.Landing)
            guiContext.hitTestRegion((400, 400))
        elif self.runCount == 11:
            self.assertTrue(guiContext.target_panel.target)
            post(Event(UI_BUTTON_PRESSED, ui_element = guiContext.target_panel.confirm_button))
        elif self.runCount == 12:
            self.assertTrue(isinstance(guiContext, OrbitContext))
            self.assertEqual(guiContext.target_mode, OCMode.LaunchPlan)
            post(Event(UI_BUTTON_PRESSED, ui_element = guiContext.target_panel.confirm_button))
        elif self.runCount == 13:
            self.assertTrue(isinstance(guiContext, ColonyContext))
            post(Event(UI_BUTTON_PRESSED, ui_element = guiContext.ship_detail_panel.launch_button))
        elif self.runCount == 14:
            post(Event(UI_BUTTON_PRESSED, ui_element = guiContext.timing_panel.start_button))
        elif self.runCount == 99:
            post(Event(UI_BUTTON_PRESSED, ui_element = guiContext.timing_panel.stop_button))
        elif self.runCount == 100:
            surface = model.planetSim.planetById("MOON").surface
            self.assertGreater(len(surface.points), 0)
            self.assertEqual(surface.points[0].name, "MSS Viking")
            self.testPassed = True
    

        if self.runCount == 120:
            self.assertTrue(self.testPassed)
            post(Event(QUIT))
        self.runCount += 1
        return
    
class SystemTestSurfaceSurfaceLaunchLand(SystemTestShipLandingLogic):
    def testSurfaceSurfaceLaunchLand(self):
        self.runCount = 0
        self.outerTestPassed = False
        spacesim.main(testingCallback=self.surfaceLaunchLandCallback)

    def surfaceLaunchLandCallback(self, model, guiContext):
        if self.runCount < 52:
            self.shipLandingLogicCallback(model, guiContext)
            return
        else:
            if self.runCount == 52:
                mercury = None
                for s in guiContext.all_sprites:
                    if not isinstance(s, OrbitNodeView):
                        continue
                    if s.node.id == "MES":
                        mercury = s

                self.assertTrue(isinstance(guiContext, OrbitContext))
                guiContext.resolveNodeClick(mercury)
            elif self.runCount == 53:
                self.assertTrue(isinstance(guiContext, OrbitContext))
                post(Event(UI_BUTTON_PRESSED, ui_element = guiContext.planet_summary.surface_button))
            elif self.runCount == 54:
                self.assertTrue(isinstance(guiContext, SurfaceContext))
                ship = None
                for s in guiContext.all_sprites:
                    if isinstance(s, SurfaceObjectSprite):
                        if isinstance(s.surfaceObject.content, Ship):
                            ship = s
                self.assertIsNotNone(ship)
                guiContext.handleClickedObject(ship)
            elif self.runCount == 55:
                self.assertTrue(isinstance(guiContext, SurfaceContext))
                post(Event(UI_BUTTON_PRESSED, ui_element = guiContext.vehicle_panel.target_button))
            elif self.runCount == 56:
                self.assertTrue(isinstance(guiContext, OrbitContext))
                moon = None
                for s in guiContext.all_sprites:
                    if not isinstance(s, OrbitNodeView):
                        continue
                    if s.node.id == "MOS":
                        moon = s
                guiContext.resolveNodeClick(moon)
            elif self.runCount == 57:
                self.assertTrue(isinstance(guiContext, OrbitContext))
                post(Event(UI_BUTTON_PRESSED, ui_element = guiContext.target_panel.surface_button))
            elif self.runCount == 58:
                self.assertTrue(isinstance(guiContext, SurfaceContext))
                self.assertEqual(guiContext.targetMode, SCMode.Landing)
                guiContext.hitTestRegion((400, 400))
            elif self.runCount == 59:
                self.assertTrue(isinstance(guiContext, SurfaceContext))
                post(Event(UI_BUTTON_PRESSED, ui_element = guiContext.target_panel.confirm_button))
            elif self.runCount == 60:
                self.assertTrue(guiContext, OrbitContext)
                post(Event(UI_BUTTON_PRESSED, ui_element = guiContext.target_panel.confirm_button))
            elif self.runCount == 61:
                self.assertTrue(guiContext, SurfaceContext)
                post(Event(UI_BUTTON_PRESSED, ui_element = guiContext.ship_panel.launch_button))
            elif self.runCount == 62:
                post(Event(UI_BUTTON_PRESSED, ui_element = guiContext.timing_panel.start_button))
            elif self.runCount == 199:
                post(Event(UI_BUTTON_PRESSED, ui_element = guiContext.timing_panel.stop_button))
            elif self.runCount == 200:
                surface = model.planetSim.planetById("MOON").surface
                self.assertGreater(len(surface.points), 0)
                self.assertEqual(surface.points[0].name, "ISS Meghalaya")
                self.outerTestPassed = True                     


        if self.runCount == 210:
            self.assertTrue(self.outerTestPassed)
            post(Event(QUIT))
        self.runCount += 1
        return

class SystemTestSurfaceColonyLaunchLand(unittest.TestCase):
    pass

class SystemTestColonyColonyLaunchLand(unittest.TestCase):
    pass

class SystemTestContextStack(unittest.TestCase):
    def testContextStack(self):
        self.runCount = 0
        self.testPassed = False
        spacesim.main(testingCallback=self.contextStackCallback)

    def contextStackCallback(self, model, guiContext):
        if isinstance(guiContext, MenuContext):
            pos = guiContext.loadItem.rect.center
            pygame.mouse.set_pos(pos)
            post(Event(MOUSEBUTTONUP))
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
                post(event)
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
                post(event)
            elif self.runCount == 6:
                post(Event(UI_BUTTON_PRESSED, ui_element = guiContext.settings_button))

        elif isinstance(guiContext, ColonyContext):
            self.assertGreater(self.runCount, 4)
            post(Event(UI_BUTTON_PRESSED, ui_element = guiContext.settings_button))

        
        if self.runCount == 30:
            self.assertTrue(self.testPassed)
            post(Event(QUIT))
        self.runCount += 1
        return