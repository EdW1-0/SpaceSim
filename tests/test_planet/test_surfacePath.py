import unittest

import math

from planetsim.surfacePath import SurfacePath, gcIntersections, pathsIntersect
from planetsim.surfacePoint import SurfacePoint, normalisePoint, latLong

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

    def testPathIsNorthPolar(self):
        self.assertTrue(SurfacePath(SurfacePoint(80.0, 50.0), SurfacePoint(80.0, 230.0)).isNorthPolar())
        self.assertTrue(SurfacePath(SurfacePoint(0.0, 50.0), SurfacePoint(0.0, 230.0)).isNorthPolar())
        self.assertTrue(SurfacePath(SurfacePoint(70.0, 50.0), SurfacePoint(-60.0, 230.0)).isNorthPolar())   
        self.assertTrue(SurfacePath(SurfacePoint(-10.0, 50.0), SurfacePoint(-10.0, 230.0), long = True).isNorthPolar())
        self.assertFalse(SurfacePath(SurfacePoint(80.0, 50.0), SurfacePoint(80.0, 230.0), long=True).isNorthPolar())
        self.assertFalse(SurfacePath(SurfacePoint(-10.0, 50.0), SurfacePoint(-10.0, 230.0)).isNorthPolar())
        self.assertFalse(SurfacePath(SurfacePoint(70.0, 50.0), SurfacePoint(80.0, 50.0)).isNorthPolar())
        self.assertFalse(SurfacePath(SurfacePoint(80.0, 50.0), SurfacePoint(80.0, 240.0)).isNorthPolar())

    def testPathIsSouthPolar(self):
        self.assertFalse(SurfacePath(SurfacePoint(80.0, 50.0), SurfacePoint(80.0, 230.0)).isSouthPolar())
        self.assertFalse(SurfacePath(SurfacePoint(0.0, 50.0), SurfacePoint(0.0, 230.0)).isSouthPolar())
        self.assertFalse(SurfacePath(SurfacePoint(70.0, 50.0), SurfacePoint(-60.0, 230.0)).isSouthPolar())   
        self.assertFalse(SurfacePath(SurfacePoint(-10.0, 50.0), SurfacePoint(-10.0, 230.0), long = True).isSouthPolar())
        self.assertTrue(SurfacePath(SurfacePoint(80.0, 50.0), SurfacePoint(80.0, 230.0), long=True).isSouthPolar())
        self.assertTrue(SurfacePath(SurfacePoint(-10.0, 50.0), SurfacePoint(-10.0, 230.0)).isSouthPolar())
        self.assertFalse(SurfacePath(SurfacePoint(70.0, 50.0), SurfacePoint(80.0, 50.0)).isSouthPolar())
        self.assertFalse(SurfacePath(SurfacePoint(80.0, 50.0), SurfacePoint(80.0, 240.0)).isSouthPolar())

    def testPathIsDoublePolar(self):
        self.assertTrue(SurfacePath(SurfacePoint(-60.0, 100.0), SurfacePoint(80.0, 100.0), long=True).isDoublePolar())
        self.assertFalse(SurfacePath(SurfacePoint(-60.0, 100.0), SurfacePoint(80.0, 100.0)).isDoublePolar())
        self.assertFalse(SurfacePath(SurfacePoint(-60.0, 110.0), SurfacePoint(80.0, 100.0), long=True).isDoublePolar())

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

class TestPathIntersections(unittest.TestCase):
    def testPathsIntersectionPoints(self):
        path1 = SurfacePath(SurfacePoint(0,0), SurfacePoint(0,90))
        path2 = SurfacePath(SurfacePoint(0,0), SurfacePoint(90,0))
        self.assertEqual(gcIntersections(path1, path2), ((1,0,0),(-1,0,0)))
        path1 = SurfacePath(SurfacePoint(50, 20), SurfacePoint(-50, 80))
        path2 = SurfacePath(SurfacePoint(-50, 20), SurfacePoint(50, 80))
        ints = tuple(normalisePoint(latLong(i)) for i in gcIntersections(path1, path2))
        self.assertAlmostEqual(ints[0].latitude, 0.0)
        self.assertAlmostEqual(ints[0].longitude, 50.0)
        self.assertEqual(ints[1], SurfacePoint(0.0, 230.0))
        #path1 = (SurfacePoint(51.5,0.1), SurfacePoint(40.7, 74.0)) # London - New York
        #path2 = (SurfacePoint(46.8, 71.2), SurfacePoint(44.6, 63.5)) # Quebec - Halifax
        #self.assertEqual(self.ps.gcIntersections(path1, path2)[1], SurfacePoint(45.2, 65.4).vector())


    def testPathsIntersectNoWrapNoSingularity(self):
        path1 = SurfacePath(SurfacePoint(50, 20), SurfacePoint(-50, 80))
        path2 = SurfacePath(SurfacePoint(-50, 20), SurfacePoint(50, 80))
        self.assertTrue(pathsIntersect(path1, path2))
        self.assertTrue(pathsIntersect(path2, path1))
        path3 = SurfacePath(SurfacePoint(-50, 80), SurfacePoint(50, 20))
        path4 = SurfacePath(SurfacePoint(50, 80), SurfacePoint(-50, 20))
        self.assertTrue(pathsIntersect(path3, path4))
        self.assertTrue(pathsIntersect(path4, path3))
        # Positive case

    def testPathsDontIntersectRespectsDirectionality(self):
        path1 = SurfacePath(SurfacePoint(-50, 80), SurfacePoint(50, 20), long=True)
        path2 = SurfacePath(SurfacePoint(-50, 20), SurfacePoint(50, 80))
        self.assertFalse(pathsIntersect(path1, path2))

    def testPathsDontIntersectNoWrapNoSingularity(self):
        path1 = SurfacePath(SurfacePoint(50, 20), SurfacePoint(-50, 80))
        path2 = SurfacePath(SurfacePoint(-50, 20), SurfacePoint(50, 10))
        self.assertFalse(pathsIntersect(path1, path2))

    def testPathsDontIntersectAntipodeOnOneArc(self):
        path1 = SurfacePath(SurfacePoint(50, 20), SurfacePoint(-50, 80))
        path2 = SurfacePath(SurfacePoint(-50, 20), SurfacePoint(-30, 30))
        self.assertFalse(pathsIntersect(path1, path2))
        
    def testPathsIntersectOnMeridian(self):
        path1 = SurfacePath(SurfacePoint(0, 20), SurfacePoint(0, 60))
        path2 = SurfacePath(SurfacePoint(-40, 40), SurfacePoint(40, 40))
        self.assertTrue(pathsIntersect(path1, path2))

    def testPathsIntersectOnDateline(self):
        path1 = SurfacePath(SurfacePoint(40, 300), SurfacePoint(-40, 60))
        path2 = SurfacePath(SurfacePoint(-40, 300), SurfacePoint(40, 60))
        self.assertTrue(pathsIntersect(path1, path2))

    def testPathsDontIntersectOnDateline(self):
        path1 = SurfacePath(SurfacePoint(40, 300), SurfacePoint(20, 60))
        path2 = SurfacePath(SurfacePoint(-40, 300), SurfacePoint(-20, 60))
        self.assertFalse(pathsIntersect(path1, path2))

    def testPathsIntersectOnMeridianCrossDateline(self):
        path1 = SurfacePath(SurfacePoint(0,300), SurfacePoint(0,40))
        path2 = SurfacePath(SurfacePoint(-40, 0), SurfacePoint(40, 0))
        self.assertTrue(pathsIntersect(path1, path2))

    def testPathsIntersectCrossingPole(self):
        path1 = SurfacePath(SurfacePoint(70, 60), SurfacePoint(70, 240))
        path2 = SurfacePath(SurfacePoint(80, 59), SurfacePoint(80, 61))
        path3 = SurfacePath(SurfacePoint(80, 239), SurfacePoint(80, 241))
        path4 = SurfacePath(SurfacePoint(70, 240), SurfacePoint(70, 60))
        path5 = SurfacePath(SurfacePoint(-80, 60), SurfacePoint(-80, 240), long=True)
        path6 = SurfacePath(SurfacePoint(70, 60), SurfacePoint(70, 240), long=True)
        self.assertTrue(pathsIntersect(path1, path2))
        self.assertTrue(pathsIntersect(path1, path3))
        self.assertTrue(pathsIntersect(path2, path1))
        self.assertTrue(pathsIntersect(path3, path1))
        self.assertTrue(pathsIntersect(path4, path2))
        self.assertTrue(pathsIntersect(path4, path3))
        self.assertTrue(pathsIntersect(path5, path3))
        self.assertTrue(pathsIntersect(path3, path5))
        self.assertFalse(pathsIntersect(path6, path3))
        self.assertFalse(pathsIntersect(path2, path6))

    def testPathsIntersectCrossingBothPoles(self):
        path1 = SurfacePath(SurfacePoint(70,60), SurfacePoint(-20, 60))
        path2 = SurfacePath(SurfacePoint(80,59), SurfacePoint(80, 61))
        path3 = SurfacePath(SurfacePoint(-40, 239), SurfacePoint(-40, 241))
        path4 = SurfacePath(SurfacePoint(-30, 59), SurfacePoint(-30, 61))
        path5 = SurfacePath(SurfacePoint(70,60), SurfacePoint(-20, 60), long=True)
        self.assertFalse(pathsIntersect(path2, path1))
        self.assertFalse(pathsIntersect(path3, path1))
        self.assertFalse(pathsIntersect(path4, path1))
        self.assertFalse(pathsIntersect(path1, path2))
        self.assertFalse(pathsIntersect(path1, path3))
        self.assertFalse(pathsIntersect(path1, path4))
        self.assertTrue(pathsIntersect(path2, path5))
        self.assertTrue(pathsIntersect(path3, path5))
        self.assertTrue(pathsIntersect(path4, path5))
        self.assertTrue(pathsIntersect(path5, path2))
        self.assertTrue(pathsIntersect(path5, path3))
        self.assertTrue(pathsIntersect(path5, path4))

    def testPathsDontIntersectCrossingBothPoles(self):
        path1 = SurfacePath(SurfacePoint(70,60), SurfacePoint(-20, 60))
        path2 = SurfacePath(SurfacePoint(80,57), SurfacePoint(80, 59))
        path3 = SurfacePath(SurfacePoint(-40, 237), SurfacePoint(-40, 239))
        path4 = SurfacePath(SurfacePoint(-30, 57), SurfacePoint(-30, 59))
        self.assertFalse(pathsIntersect(path2, path1))
        self.assertFalse(pathsIntersect(path3, path1))
        self.assertFalse(pathsIntersect(path4, path1))
        self.assertFalse(pathsIntersect(path1, path2))
        self.assertFalse(pathsIntersect(path1, path3))
        self.assertFalse(pathsIntersect(path1, path4))
        # Negative - antipodes on neither arc /
        # Negative - antipodes on one are /
        # Edge cases
        # Crosses date line /
        # Works for either direction of path/
        # Crosses pole
        # Crosses south pole
        # Crosses both poles
        # Equatorial