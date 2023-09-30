import unittest

from planetsim.surfaceRegion import SurfaceRegion
from planetsim.surfacePoint import SurfacePoint
from planetsim.surfacePath import SurfacePath


class TestSurfaceRegion(unittest.TestCase):
    def setUp(self):
        b1 = SurfacePath(SurfacePoint(-30, -30), SurfacePoint(-30, 30))
        b2 = SurfacePath(SurfacePoint(-30, 30), SurfacePoint(30, 0))
        b3 = SurfacePath(SurfacePoint(30, 0), SurfacePoint(-30, -30))
        self.triangle = [b1, b2, b3]

    def testSurfaceRegion(self):
        self.assertTrue(SurfaceRegion)
        self.assertTrue(SurfaceRegion(0, [], []))
        self.assertTrue(SurfaceRegion(0, [], [], name="Belgium", terrain="WAFFLE"))

    def testSurfaceAttributes(self):
        self.assertTrue(hasattr(SurfaceRegion(0, [], []), "id"))
        self.assertTrue(hasattr(SurfaceRegion(0, [], []), "borders"))
        self.assertTrue(hasattr(SurfaceRegion(0, [], []), "homePoint"))
        self.assertTrue(hasattr(SurfaceRegion(0, [], []), "name"))
        self.assertTrue(hasattr(SurfaceRegion(0, [], []), "terrain"))

    def testSurfacePathConstructor(self):
        self.assertEqual(SurfaceRegion(7, [], []).id, 7)
        self.assertEqual(
            SurfaceRegion(3, SurfacePoint(30.0, 30.0), []).homePoint,
            SurfacePoint(30.0, 30.0),
        )

        self.assertEqual(
            SurfaceRegion(3, SurfacePoint(0.0, 0.0), self.triangle).borders[0].p1,
            SurfacePoint(-30, -30),
        )
        self.assertEqual(
            SurfaceRegion(3, SurfacePoint(0.0, 0.0), self.triangle).borders[1].p1,
            SurfacePoint(-30, 30),
        )
        self.assertEqual(
            SurfaceRegion(3, SurfacePoint(0.0, 0.0), self.triangle).borders[2].p1,
            SurfacePoint(30, 0),
        )


class TestRegionHitTesting(unittest.TestCase):
    def setUp(self):
        b1 = SurfacePath(SurfacePoint(-30, -30), SurfacePoint(-30, 30))
        b2 = SurfacePath(SurfacePoint(-30, 30), SurfacePoint(30, 0))
        b3 = SurfacePath(SurfacePoint(30, 0), SurfacePoint(-30, -30))
        self.triangle = [b1, b2, b3]
        self.region = SurfaceRegion(3, SurfacePoint(0.0, 0.0), self.triangle)

    def testPointInRegion(self):
        self.assertTrue(self.region.pointInRegion(SurfacePoint(10.0, 0.0)))

    def testPointOutOfRegion(self):
        self.assertFalse(self.region.pointInRegion(SurfacePoint(50.0, 50.0)))
