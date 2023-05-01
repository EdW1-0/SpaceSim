from views.surfaceContext import SurfaceContext
from views.guiContext import GUIContext

import unittest
from tests.test_views.test_guiContext import ScreenMock, ModelMock

import pygame
import pygame_gui

class SurfaceMock:
    def __init__(self):
        self.points = {}
        self.regions = {}

class PlanetMock:
    def __init__(self):
        self.surface = SurfaceMock()
        self.name = "Test Planet"
        self.gravity = 14

class ModelMock:
    pass

class TestSurfaceContext(unittest.TestCase):
    def setUp(self):
        self.mm = ModelMock()
        tm = ModelMock()
        self.mm.timingMaster = tm
        pygame.init()
        self.manager = pygame_gui.UIManager((1200, 800))
        screen = pygame.display.set_mode((1200, 800))

    def testSurfaceContext(self):
        self.assertTrue(SurfaceContext)
        self.assertTrue(SurfaceContext(None, self.mm, self.manager, PlanetMock()))

    def testSurfaceContextCoordinateConversion(self):
        sc = SurfaceContext(None, self.mm, self.manager, PlanetMock())
        self.assertEqual((500,400), sc.latLongToXY(sc.xyToLatLong((500,400))))
        p1 = (400, 300)
        p2 = sc.latLongToXY(sc.xyToLatLong((400,300)))
        self.assertAlmostEqual(p1[0], p2[0])
        self.assertAlmostEqual(p1[1], p2[1])

        p1 = (30, 30)
        p2 = sc.xyToLatLong(sc.latLongToXY((30, 30)))
        self.assertAlmostEqual(p1[0], p2[0])
        self.assertAlmostEqual(p1[1], p2[1])
        