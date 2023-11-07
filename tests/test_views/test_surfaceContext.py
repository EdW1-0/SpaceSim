from views.surfaceContext import (
    SurfaceContext,
    SurfaceObjectSprite,
    SurfaceDestinationSprite,
    SELECTED_REGION_COLOUR,
)

import unittest
from tests.test_views.test_guiContext import ModelMock

from planetsim.surfacePoint import SurfacePoint

from gameModel import GameModel

import pygame
import pygame_gui

import sys
def isLocal():
    return sys.platform.startswith("win"), "requires Windows"


class SurfaceMock:
    def __init__(self):
        self.points = {}
        self.regions = {}


class PlanetMock:
    def __init__(self):
        self.surface = SurfaceMock()
        self.name = "Test Planet"
        self.gravity = 14

@unittest.skipUnless(isLocal())
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

@unittest.skipUnless(isLocal())
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

@unittest.skipUnless(isLocal())
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

@unittest.skipUnless(isLocal())
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
