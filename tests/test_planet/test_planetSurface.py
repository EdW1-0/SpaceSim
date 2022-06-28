import unittest

import math

from planetsim.planetSurface import PlanetSurface, EARTH_RADIUS
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

    def testGreatCircleAngle(self):
        self.assertEqual(self.ps.gcAngle(SurfacePoint(0.0, 0.0), SurfacePoint(0.0, 0.0)), 0.0)
        self.assertEqual(self.ps.gcAngle(SurfacePoint(0.0, 0.0), SurfacePoint(90.0, 0.0)), math.pi/2)
        self.assertEqual(self.ps.gcAngle(SurfacePoint(0.0, 0.0), SurfacePoint(0.0, 180.0)), math.pi)

    def testGreatCircleDistance(self):
        self.assertAlmostEqual(self.ps.gcDistance(SurfacePoint(90.0, 0.0), SurfacePoint(0.0,0.0)), 10007543, delta = 1)
        self.assertAlmostEqual(self.ps.gcDistance(SurfacePoint(0.0, 0.0), SurfacePoint(0.0,180.0)), 20015086, delta = 1)
        london = SurfacePoint(51.5,0.1)
        oxford = SurfacePoint(51.7,1.2)
        newYork = SurfacePoint(40.7, 74.0)
        self.assertAlmostEqual(self.ps.gcDistance(london, newYork), 5585000, delta = 20000)
        self.assertAlmostEqual(self.ps.gcDistance(london, oxford), 81890, delta = 5000)

class TestIntersectionTesting(unittest.TestCase):
    def setUp(self):
        self.ps = PlanetSurface("test_json/test_surfaces/single_region.json")
        self.twor = PlanetSurface("test_json/test_surfaces/2_hemispheres.json")

    def testPathsIntersectionPoints(self):
        path1 = (SurfacePoint(0,0), SurfacePoint(0,90))
        path2 = (SurfacePoint(0,0), SurfacePoint(90,0))
        self.assertEqual(self.ps.gcIntersections(path1, path2), ((1,0,0),(-1,0,0)))
        path1 = (SurfacePoint(50, 20), SurfacePoint(-50, 80))
        path2 = (SurfacePoint(-50, 20), SurfacePoint(50, 80))
        ints = tuple(normalisePoint(latLong(i)) for i in self.ps.gcIntersections(path1, path2))
        self.assertAlmostEqual(ints[0].latitude, 0.0)
        self.assertAlmostEqual(ints[0].longitude, 50.0)
        self.assertEqual(ints[1], SurfacePoint(0.0, 230.0))
        #path1 = (SurfacePoint(51.5,0.1), SurfacePoint(40.7, 74.0)) # London - New York
        #path2 = (SurfacePoint(46.8, 71.2), SurfacePoint(44.6, 63.5)) # Quebec - Halifax
        #self.assertEqual(self.ps.gcIntersections(path1, path2)[1], SurfacePoint(45.2, 65.4).vector())

    def testPathsIntersectNoWrapNoSingularity(self):
        path1 = (SurfacePoint(50, 20), SurfacePoint(-50, 80))
        path2 = (SurfacePoint(-50, 20), SurfacePoint(50, 80))
        self.assertTrue(self.ps.pathsIntersect(path1, path2))
        # Positive case

    def testPathsDontIntersectNoWrapNoSingularity(self):
        path1 = (SurfacePoint(50, 20), SurfacePoint(-50, 80))
        path2 = (SurfacePoint(-50, 20), SurfacePoint(50, 10))
        self.assertFalse(self.ps.pathsIntersect(path1, path2))

    def testPathsDontIntersectAntipodeOnOneArc(self):
        path1 = (SurfacePoint(50, 20), SurfacePoint(-50, 80))
        path2 = (SurfacePoint(-50, 20), SurfacePoint(-30, 30))
        self.assertFalse(self.ps.pathsIntersect(path1, path2))
        
        
    def testPathsIntersectOnMeridian(self):
        path1 = (SurfacePoint(0,300), SurfacePoint(0,40))
        path2 = (SurfacePoint(-40, 0), SurfacePoint(40, 0))
        self.assertTrue(self.ps.pathsIntersect(path1, path2))
        # Negative - antipodes on neither arc
        # Negative - antipodes on one are
        # Edge cases

    def testPointInRegion(self):
        pass