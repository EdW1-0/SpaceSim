from views.surfaceContext import SurfaceContext
from views.guiContext import GUIContext

import unittest
from tests.test_views.test_guiContext import ScreenMock, ModelMock

import pygame

class SurfaceMock:
    def __init__(self):
        self.points = {}
        self.regions = {}

class PlanetMock:
    def __init__(self):
        self.surface = SurfaceMock()

class TestSurfaceContext(unittest.TestCase):
    def testSurfaceContext(self):
        self.assertTrue(SurfaceContext)
        self.assertTrue(SurfaceContext(None, None, None, PlanetMock()))

    def testSurfaceContextCoordinateConversion(self):
        sc = SurfaceContext(None, None, None, PlanetMock())
        self.assertEqual((500,400), sc.latLongToXY(sc.xyToLatLong((500,400))))
        p1 = (400, 300)
        p2 = sc.latLongToXY(sc.xyToLatLong((400,300)))
        self.assertAlmostEqual(p1[0], p2[0])
        self.assertAlmostEqual(p1[1], p2[1])

        p1 = (30, 30)
        p2 = sc.xyToLatLong(sc.latLongToXY((30, 30)))
        self.assertAlmostEqual(p1[0], p2[0])
        self.assertAlmostEqual(p1[1], p2[1])
        