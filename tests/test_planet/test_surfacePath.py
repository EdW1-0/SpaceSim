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

    def testPathIsMeridian(self):
        self.assertTrue(SurfacePath(SurfacePoint(0.0, 0.0), SurfacePoint(80.0,0.0)).isMeridian())
        self.assertFalse(SurfacePath(SurfacePoint(0.0, 0.0), SurfacePoint(80.0, 10.0)).isMeridian())
        self.assertTrue(SurfacePath(SurfacePoint(70.0, 0.0), SurfacePoint(70.0, 180.0)).isMeridian())
        self.assertTrue(SurfacePath(SurfacePoint(-70.0, 0.0), SurfacePoint(-60.0, 180.0)).isMeridian())

    def testPathCrossesDateline(self):
        self.assertTrue(SurfacePath(SurfacePoint(0.0, 340.0), SurfacePoint(80.0,20.0)).crossesDateline())
        self.assertFalse(SurfacePath(SurfacePoint(0.0, 40.0), SurfacePoint(80.0,60.0)).crossesDateline())
        self.assertFalse(SurfacePath(SurfacePoint(0.0, 340.0), SurfacePoint(80.0,60.0), long=True).crossesDateline())
        self.assertTrue(SurfacePath(SurfacePoint(0.0, 90.0), SurfacePoint(10.0,110.0), long=True).crossesDateline())


class TestPointOnPath(unittest.TestCase):
    def setUp(self):
        self.path = SurfacePath(SurfacePoint(-20, 20), SurfacePoint(40, 80))
        self.datelinePath = SurfacePath(SurfacePoint(-20, 340), SurfacePoint(20, 20))
        self.meridianPath = SurfacePath(SurfacePoint(-20, 40), SurfacePoint(20, 40))
        self.polarPath = SurfacePath(SurfacePoint(70, 30), SurfacePoint(70, 210))
        self.southPolarPath = SurfacePath(SurfacePoint(-70, 30), SurfacePoint(-70, 210))
        self.polarWrappingPath = SurfacePath(SurfacePoint(40, 30), SurfacePoint(-40, 30), long=True)

    def testPointOnPath(self):
        self.assertTrue(self.path.pointOnPath(SurfacePoint(0,50)))
        self.assertTrue(self.datelinePath.pointOnPath(SurfacePoint(0,0)))

    def testPointNotOnPath(self):
        self.assertFalse(self.path.pointOnPath(SurfacePoint(0,0)))
        self.assertFalse(self.path.pointOnPath(SurfacePoint(-20, 110)))
