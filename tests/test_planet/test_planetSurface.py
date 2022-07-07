import unittest

import math

from planetsim.planetSurface import PlanetSurface, EARTH_RADIUS
from planetsim.surfacePath import SurfacePath
from planetsim.surfacePoint import SurfacePoint, latLong, normalisePoint

class TestPlanetSurface(unittest.TestCase):
    def testPlanetSurfaceModule(self):
        self.assertTrue(PlanetSurface)
        self.assertTrue(PlanetSurface())

    def testPlanetSurfaceAttributes(self):
        self.assertTrue(hasattr(PlanetSurface(), "regions"))
        self.assertTrue(hasattr(PlanetSurface(), "points"))
        self.assertTrue(hasattr(PlanetSurface(), "radius"))

    def testPlanetSurfaceConstructor(self):
        self.assertTrue(PlanetSurface("test_json/test_surfaces/single_region.json"))
        self.assertEqual(PlanetSurface("test_json/test_surfaces/single_region.json").radius, EARTH_RADIUS)
        
        
class TestPlanetSurfaceLoading(unittest.TestCase):
    def setUp(self):
        self.ps = PlanetSurface("test_json/test_surfaces/single_region.json")
        self.twor = PlanetSurface("test_json/test_surfaces/2_hemispheres.json")

    def testPlanetSurfaceRegionLoading(self):
        self.assertEqual(len(self.ps.regions), 1)
        self.assertEqual(len(self.twor.regions), 2)
        self.assertIsInstance(self.ps.regions[0].homePoint, SurfacePoint)
        self.assertEqual(len(self.ps.regions[0].borders), 3)
        for b in self.ps.regions[0].borders:
            self.assertIsInstance(b, SurfacePoint)

class TestGreatCircleGeodetics(unittest.TestCase):
    def setUp(self):
        self.ps = PlanetSurface("test_json/test_surfaces/single_region.json")
        self.twor = PlanetSurface("test_json/test_surfaces/2_hemispheres.json")



    def testGreatCircleDistance(self):
        self.assertAlmostEqual(self.ps.gcDistance(SurfacePath(SurfacePoint(90.0, 0.0), SurfacePoint(0.0,0.0))), 10007543, delta = 1)
        self.assertAlmostEqual(self.ps.gcDistance(SurfacePath(SurfacePoint(0.0, 0.0), SurfacePoint(0.0,180.0))), 20015086, delta = 1)
        london = SurfacePoint(51.5,0.1)
        oxford = SurfacePoint(51.7,1.2)
        newYork = SurfacePoint(40.7, 74.0)
        self.assertAlmostEqual(self.ps.gcDistance(SurfacePath(london, newYork)), 5585000, delta = 20000)
        self.assertAlmostEqual(self.ps.gcDistance(SurfacePath(london, oxford)), 81890, delta = 5000)

class TestIntersectionTesting(unittest.TestCase):
    def setUp(self):
        self.ps = PlanetSurface("test_json/test_surfaces/single_region.json")
        self.twor = PlanetSurface("test_json/test_surfaces/2_hemispheres.json")



    def testPathsIntersectNoWrapNoSingularity(self):
        path1 = SurfacePath(SurfacePoint(50, 20), SurfacePoint(-50, 80))
        path2 = SurfacePath(SurfacePoint(-50, 20), SurfacePoint(50, 80))
        self.assertTrue(self.ps.pathsIntersect(path1, path2))
        self.assertTrue(self.ps.pathsIntersect(path2, path1))
        path3 = SurfacePath(SurfacePoint(-50, 80), SurfacePoint(50, 20))
        path4 = SurfacePath(SurfacePoint(50, 80), SurfacePoint(-50, 20))
        self.assertTrue(self.ps.pathsIntersect(path3, path4))
        self.assertTrue(self.ps.pathsIntersect(path4, path3))
        # Positive case

    def testPathsDontIntersectRespectsDirectionality(self):
        path1 = SurfacePath(SurfacePoint(-50, 80), SurfacePoint(50, 20), long=True)
        path2 = SurfacePath(SurfacePoint(-50, 20), SurfacePoint(50, 80))
        self.assertFalse(self.ps.pathsIntersect(path1, path2))

    def testPathsDontIntersectNoWrapNoSingularity(self):
        path1 = SurfacePath(SurfacePoint(50, 20), SurfacePoint(-50, 80))
        path2 = SurfacePath(SurfacePoint(-50, 20), SurfacePoint(50, 10))
        self.assertFalse(self.ps.pathsIntersect(path1, path2))

    def testPathsDontIntersectAntipodeOnOneArc(self):
        path1 = SurfacePath(SurfacePoint(50, 20), SurfacePoint(-50, 80))
        path2 = SurfacePath(SurfacePoint(-50, 20), SurfacePoint(-30, 30))
        self.assertFalse(self.ps.pathsIntersect(path1, path2))
        
    def testPathsIntersectOnMeridian(self):
        path1 = SurfacePath(SurfacePoint(0, 20), SurfacePoint(0, 60))
        path2 = SurfacePath(SurfacePoint(-40, 40), SurfacePoint(40, 40))
        self.assertTrue(self.ps.pathsIntersect(path1, path2))

    def testPathsIntersectOnDateline(self):
        path1 = SurfacePath(SurfacePoint(40, 300), SurfacePoint(-40, 60))
        path2 = SurfacePath(SurfacePoint(-40, 300), SurfacePoint(40, 60))
        self.assertTrue(self.ps.pathsIntersect(path1, path2))

    def testPathsDontIntersectOnDateline(self):
        path1 = SurfacePath(SurfacePoint(40, 300), SurfacePoint(20, 60))
        path2 = SurfacePath(SurfacePoint(-40, 300), SurfacePoint(-20, 60))
        self.assertFalse(self.ps.pathsIntersect(path1, path2))

    def testPathsIntersectOnMeridianCrossDateline(self):
        path1 = SurfacePath(SurfacePoint(0,300), SurfacePoint(0,40))
        path2 = SurfacePath(SurfacePoint(-40, 0), SurfacePoint(40, 0))
        self.assertTrue(self.ps.pathsIntersect(path1, path2))

    def testPathsIntersectCrossingPole(self):
        path1 = SurfacePath(SurfacePoint(70, 60), SurfacePoint(70, 240))
        path2 = SurfacePath(SurfacePoint(80, 59), SurfacePoint(80, 61))
        path3 = SurfacePath(SurfacePoint(80, 239), SurfacePoint(80, 241))
        path4 = SurfacePath(SurfacePoint(70, 240), SurfacePoint(70, 60))
        path5 = SurfacePath(SurfacePoint(-80, 60), SurfacePoint(-80, 240), long=True)
        path6 = SurfacePath(SurfacePoint(70, 60), SurfacePoint(70, 240), long=True)
        self.assertTrue(self.ps.pathsIntersect(path1, path2))
        self.assertTrue(self.ps.pathsIntersect(path1, path3))
        self.assertTrue(self.ps.pathsIntersect(path2, path1))
        self.assertTrue(self.ps.pathsIntersect(path3, path1))
        self.assertTrue(self.ps.pathsIntersect(path4, path2))
        self.assertTrue(self.ps.pathsIntersect(path4, path3))
        self.assertTrue(self.ps.pathsIntersect(path5, path3))
        self.assertTrue(self.ps.pathsIntersect(path3, path5))
        self.assertFalse(self.ps.pathsIntersect(path6, path3))
        self.assertFalse(self.ps.pathsIntersect(path2, path6))

    def testPathsIntersectCrossingBothPoles(self):
        path1 = SurfacePath(SurfacePoint(70,60), SurfacePoint(-20, 60))
        path2 = SurfacePath(SurfacePoint(80,59), SurfacePoint(80, 61))
        path3 = SurfacePath(SurfacePoint(-40, 239), SurfacePoint(-40, 241))
        path4 = SurfacePath(SurfacePoint(-30, 59), SurfacePoint(-30, 61))
        path5 = SurfacePath(SurfacePoint(70,60), SurfacePoint(-20, 60), long=True)
        self.assertFalse(self.ps.pathsIntersect(path2, path1))
        self.assertFalse(self.ps.pathsIntersect(path3, path1))
        self.assertFalse(self.ps.pathsIntersect(path4, path1))
        self.assertFalse(self.ps.pathsIntersect(path1, path2))
        self.assertFalse(self.ps.pathsIntersect(path1, path3))
        self.assertFalse(self.ps.pathsIntersect(path1, path4))
        self.assertTrue(self.ps.pathsIntersect(path2, path5))
        self.assertTrue(self.ps.pathsIntersect(path3, path5))
        self.assertTrue(self.ps.pathsIntersect(path4, path5))
        self.assertTrue(self.ps.pathsIntersect(path5, path2))
        self.assertTrue(self.ps.pathsIntersect(path5, path3))
        self.assertTrue(self.ps.pathsIntersect(path5, path4))

    def testPathsDontIntersectCrossingBothPoles(self):
        path1 = SurfacePath(SurfacePoint(70,60), SurfacePoint(-20, 60))
        path2 = SurfacePath(SurfacePoint(80,57), SurfacePoint(80, 59))
        path3 = SurfacePath(SurfacePoint(-40, 237), SurfacePoint(-40, 239))
        path4 = SurfacePath(SurfacePoint(-30, 57), SurfacePoint(-30, 59))
        self.assertFalse(self.ps.pathsIntersect(path2, path1))
        self.assertFalse(self.ps.pathsIntersect(path3, path1))
        self.assertFalse(self.ps.pathsIntersect(path4, path1))
        self.assertFalse(self.ps.pathsIntersect(path1, path2))
        self.assertFalse(self.ps.pathsIntersect(path1, path3))
        self.assertFalse(self.ps.pathsIntersect(path1, path4))
        # Negative - antipodes on neither arc /
        # Negative - antipodes on one are /
        # Edge cases
        # Crosses date line /
        # Works for either direction of path/
        # Crosses pole
        # Crosses south pole
        # Crosses both poles
        # Equatorial


class TestPlanetRegionTesting(unittest.TestCase):
    def setUp(self):
        self.ps = PlanetSurface("test_json/test_surfaces/single_region.json")
        self.twor = PlanetSurface("test_json/test_surfaces/2_hemispheres.json")

    def testPointInRegion(self):
        r = self.ps.regions[0]
        p = SurfacePoint(0.0,0.0)
        #self.assertTrue(r.pointInRegion(p))