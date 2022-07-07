import unittest

import math

from planetsim.planetSurface import PlanetSurface, EARTH_RADIUS
from planetsim.surfacePath import SurfacePath, pathsIntersect
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






class TestPlanetRegionTesting(unittest.TestCase):
    def setUp(self):
        self.ps = PlanetSurface("test_json/test_surfaces/single_region.json")
        self.twor = PlanetSurface("test_json/test_surfaces/2_hemispheres.json")

