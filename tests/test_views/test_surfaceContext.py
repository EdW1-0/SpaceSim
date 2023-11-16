from views.surfaceContext import (
    SurfaceContext,
    SurfaceObjectSprite,
    SurfaceDestinationSprite,
    SELECTED_REGION_COLOUR,
)

import unittest
from tests.test_views.test_guiContext import ModelMock, isLocal

from planetsim.surfacePoint import SurfacePoint

from gameModel import GameModel

import pygame
import pygame_gui

from pygame.locals import (
    K_DOWN,
    K_UP,
    K_LEFT, 
    K_RIGHT
)



class SurfaceMock:
    def __init__(self):
        self.points = {}
        self.regions = {}


class PlanetMock:
    def __init__(self):
        self.surface = SurfaceMock()
        self.name = "Test Planet"
        self.gravity = 14

@unittest.skipUnless(isLocal(), "requires Windows")
class TestSurfaceObjectSprite(unittest.TestCase):
    def testSurfaceObjectSprite(self):
        self.assertTrue(SurfaceObjectSprite)

    def testSurfaceObjectSpriteConstructor(self):
        so = ModelMock()
        sp = ModelMock()
        so.point = sp
        self.assertTrue(SurfaceObjectSprite(so))
        self.assertTrue(SurfaceObjectSprite(so, (20, 20)))
        self.assertTrue(SurfaceObjectSprite(so, center=(1, 1), selected=True))

    def testSurfaceObjectSpriteLatLong(self):
        so = ModelMock()
        sp = SurfacePoint(30, 40)
        so.point = sp
        sprite = SurfaceObjectSprite(so)
        self.assertEqual(sprite.latLong(), (30, 40))

@unittest.skipUnless(isLocal(), "requires Windows")
class TestSurfaceDestinationSprite(unittest.TestCase):
    def testSurfaceDestinationSprite(self):
        self.assertTrue(SurfaceDestinationSprite)

    def testSurfaceDestinationSpriteConstructor(self):
        self.assertTrue(SurfaceDestinationSprite())
        self.assertTrue(SurfaceDestinationSprite(center=(7, 7)))

    def testSurfaceDestinationSpriteLatLong(self):
        so = ModelMock()
        sp = SurfacePoint(5, 10)
        so.destination = sp
        sds = SurfaceDestinationSprite()
        sds.surfaceObject = so
        self.assertEqual(sds.latLong(), (5, 10))

@unittest.skipUnless(isLocal(), "requires Windows")
class TestSurfaceContext(unittest.TestCase):
    def setUp(self):
        self.mm = ModelMock()
        tm = ModelMock()
        self.mm.timingMaster = tm
        pygame.init()
        self.manager = pygame_gui.UIManager((1200, 800))
        pygame.display.set_mode((1200, 800))
        self.model = GameModel()
        self.model.load()

    def testSurfaceContext(self):
        self.assertTrue(SurfaceContext)
        self.assertTrue(
            SurfaceContext(
                None,
                self.model,
                self.manager,
                "MERCURY",
            )
        )

    def testSurfaceContextCoordinateConversion(self):
        sc = SurfaceContext(
            None, self.model, self.manager, "MERCURY"
        )
        self.assertEqual((500, 400), sc.latLongToXY(sc.xyToLatLong((500, 400))))
        p1 = (400, 300)
        p2 = sc.latLongToXY(sc.xyToLatLong((400, 300)))
        self.assertAlmostEqual(p1[0], p2[0])
        self.assertAlmostEqual(p1[1], p2[1])

        p1 = (30, 30)
        p2 = sc.xyToLatLong(sc.latLongToXY((30, 30)))
        self.assertAlmostEqual(p1[0], p2[0])
        self.assertAlmostEqual(p1[1], p2[1])

@unittest.skipUnless(isLocal(), "requires Windows")
class TestSurfaceContextGraphics(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.manager = pygame_gui.UIManager((1200, 800))
        pygame.display.set_mode((1200, 800))
        self.model = GameModel()
        self.model.load()

    def testSurfaceContextComputeRegionColour(self):
        sc = SurfaceContext(
            None, self.model, self.manager, self.model.planetSim.planetById("MERCURY").id
        )
        r = self.model.planetSim.planetById("MERCURY").surface.regionById(1)
        sc.computeRegionColour(r)

        self.assertEqual(sc.regionColours[r.id], [150, 10, 10])
        sc.selectedObject = r
        sc.computeRegionColour(r)
        self.assertEqual(sc.regionColours[r.id], SELECTED_REGION_COLOUR)

    def testSurfaceContextExtractPolygons(self):
        sc = SurfaceContext(
            None, self.model, self.manager, self.model.planetSim.planetById("MERCURY").id
        )
        pc = sc.polyCount
        sc.extractPolygons()
        pc2 = sc.polyCount
        self.assertEqual(pc2 - pc, 8)

class TestSurfaceContextCoordinateSystems(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.manager = pygame_gui.UIManager((1200, 800))
        pygame.display.set_mode((1200, 800))
        self.model = GameModel()
        self.model.load()
        self.sc = SurfaceContext(
            None, 
            self.model, 
            self.manager, 
            self.model.planetSim.planetById("MERCURY").id, 
            meridian = (30, 50))

    def testMeridianLatitude(self):
        self.assertEqual(self.sc.meridian[0], 30)
        self.sc.meridianLatitude(20)
        self.assertEqual(self.sc.meridian[0], 50)
        self.sc.meridianLatitude(50)
        self.assertEqual(self.sc.meridian[0], 90)
        self.sc.meridianLatitude(-200)
        self.assertEqual(self.sc.meridian[0], -90)

    def testMeridianLongitude(self):
        self.assertEqual(self.sc.meridian[1], 50)
        self.sc.meridianLongitude(20)
        self.assertEqual(self.sc.meridian[1], 70)
        self.sc.meridianLongitude(-80)
        self.assertEqual(self.sc.meridian[1], 350)
        self.sc.meridianLongitude(810)
        self.assertEqual(self.sc.meridian[1], 80)


class TestSurfaceContextEventHandling(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.manager = pygame_gui.UIManager((1200, 800))
        pygame.display.set_mode((1200, 800))
        self.model = GameModel()
        self.model.load()
        self.sc = SurfaceContext(
            None, 
            self.model, 
            self.manager, 
            self.model.planetSim.planetById("MERCURY").id, 
            meridian = (30, 50))
        
    def testHandleMouseWheel(self):
        event = ModelMock()
        event.y = 50.0
        self.assertEqual(self.sc.radius, 300.0)
        self.sc.handleMouseWheel(event)
        self.assertEqual(self.sc.radius, 200.0)
        event.y = -10.0
        self.sc.handleMouseWheel(event)
        self.sc.handleMouseWheel(event)
        self.assertEqual(self.sc.radius, 400.0)        

    def testHandleKeyPress(self):
        event = ModelMock()
        self.assertEqual(self.sc.meridian, (30, 50))

        event.key = K_UP
        self.sc.handleKeyPress(event)
        self.assertEqual(self.sc.meridian, (50, 50))

        event.key = K_LEFT
        self.sc.handleKeyPress(event)
        self.assertEqual(self.sc.meridian, (50, 70))

        event.key = K_DOWN
        self.sc.handleKeyPress(event)
        self.assertEqual(self.sc.meridian, (30, 70))

        event.key = K_RIGHT
        self.sc.handleKeyPress(event)
        self.assertEqual(self.sc.meridian, (30, 50))