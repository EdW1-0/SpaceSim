import unittest

import math

from planetsim.surfacePath import SurfacePath
from planetsim.surfacePoint import SurfacePoint

class TestSurfacePath(unittest.TestCase):
    def testSurfacePathInit(self):
        self.assertTrue(SurfacePath)
        self.assertTrue(SurfacePath(SurfacePoint(0,0), SurfacePoint(0,0)))

    def testSurfacePathAttributes(self):
        self.assertTrue(hasattr(SurfacePath(), "p1"))
        self.assertTrue(hasattr(SurfacePath(), "p2"))
        self.assertTrue(hasattr(SurfacePath(), "long"))

    def testSurfacePathConstructor(self):
        self.assertEqual(SurfacePath(p1 = SurfacePoint(30, 60)).p1, SurfacePoint(30, 60))
        self.assertEqual(SurfacePath(p2 = SurfacePoint(-40, 270)).p2, SurfacePoint(-40, 270))
        self.assertEqual(SurfacePath().long, False)
        self.assertEqual(SurfacePath(long = True).long, True)

class TestSurfacePathGeodetics(unittest.TestCase):
    def testGreatCircleAngle(self):
        self.assertEqual(SurfacePath(SurfacePoint(0.0, 0.0), SurfacePoint(0.0, 0.0)).gcAngle(), 0.0)
        self.assertEqual(SurfacePath(SurfacePoint(0.0, 0.0), SurfacePoint(90.0, 0.0)).gcAngle(), math.pi/2)
        self.assertEqual(SurfacePath(SurfacePoint(0.0, 0.0), SurfacePoint(0.0, 180.0)).gcAngle(), math.pi)