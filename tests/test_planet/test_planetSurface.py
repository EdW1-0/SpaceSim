import unittest

import math

from planetsim.planetSurface import PlanetSurface, EARTH_RADIUS
from planetsim.surfacePath import SurfacePath
from planetsim.surfacePoint import SurfacePoint, almostEqual

class TestPlanetSurface(unittest.TestCase):
    def testPlanetSurfaceModule(self):
        self.assertTrue(PlanetSurface)
        self.assertTrue(PlanetSurface())

    def testPlanetSurfaceAttributes(self):
        self.assertTrue(hasattr(PlanetSurface(), "regions"))
        self.assertTrue(hasattr(PlanetSurface(), "points"))
        self.assertTrue(hasattr(PlanetSurface(), "radius"))
        self.assertTrue(isinstance(PlanetSurface().regions, dict))
        self.assertTrue(isinstance(PlanetSurface().points, dict))


    def testPlanetSurfaceConstructor(self):
        self.assertTrue(PlanetSurface("test_json/test_surfaces/single_region.json"))
        self.assertEqual(PlanetSurface("test_json/test_surfaces/single_region.json").radius, EARTH_RADIUS)
        
        
class TestPlanetSurfaceLoading(unittest.TestCase):
    def setUp(self):
        self.ps = PlanetSurface("test_json/test_surfaces/single_region.json")
        self.twor = PlanetSurface("test_json/test_surfaces/2_hemispheres.json")
        self.fulltile = PlanetSurface("test_json/test_surfaces/full_tiling.json")

    def testPlanetSurfaceRegionLoading(self):
        self.assertEqual(len(self.ps.regions), 1)
        self.assertEqual(len(self.twor.regions), 2)
        self.assertIsInstance(self.ps.regions[0].homePoint, SurfacePoint)
        self.assertEqual(len(self.ps.regions[0].borders), 3)
        for b in self.ps.regions[0].borders:
            self.assertIsInstance(b, SurfacePath)
        self.assertEqual(len(self.fulltile.regions), 8)
        self.assertEqual(self.fulltile.regions[3].borders[1], SurfacePath(SurfacePoint(70,0),SurfacePoint(0,0)))

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

    def testAngleForDistance(self):
        self.assertEqual(self.ps._angleForDistance(1000), 1000.0/self.ps.radius)
        self.assertEqual(self.ps._angleForDistance(2000), 2000/self.ps.radius)

class TestPlanetSurfaceIdLookup(unittest.TestCase):
    def setUp(self):
        self.ps = PlanetSurface("test_json/test_surfaces/single_region.json")
        self.twor = PlanetSurface("test_json/test_surfaces/2_hemispheres.json")
        self.ft = PlanetSurface("test_json/test_surfaces/full_tiling.json")

    def testRegionIdLookup(self):
        self.assertEqual(self.ft.regionById(3).id, 3)

    def testPointIdLookup(self):
        self.ft.createObject(None, SurfacePoint(10,10))
        self.assertEqual(self.ft.pointById(0).id, 0)




class TestPlanetSurfaceObjectLifecycle(unittest.TestCase):
    def setUp(self):
        self.ps = PlanetSurface("test_json/test_surfaces/single_region.json")
        self.twor = PlanetSurface("test_json/test_surfaces/2_hemispheres.json")
        self.ft = PlanetSurface("test_json/test_surfaces/full_tiling.json")

    def testSurfaceObjectCreation(self):
        self.ft.createObject(None, SurfacePoint(20, 20))
        self.assertEqual(len(self.ft.points), 1)

    def testSurfaceObjectDestruction(self):
        self.ft.createObject(None, SurfacePoint(20, 20))
        self.assertEqual(len(self.ft.points), 1)
        self.ft.destroyObject(0)
        self.assertEqual(len(self.ft.points), 0)


class TestPlanetSurfaceObjectMovement(unittest.TestCase):
    def setUp(self):
        self.ft = PlanetSurface("test_json/test_surfaces/full_tiling.json")
        self.ft.createObject(None, SurfacePoint(20,20))
        self.pt = self.ft.pointById(0)
        


    def testSurfaceObjectNilMovement(self):
        self.pt.setDestination(SurfacePoint(80, 100))
        self.assertEqual(self.ft._distanceForTime(0, 100), 0)

    def testSurfaceObjectFiniteMovement(self):
        self.pt.maxV = 20
        self.assertEqual(self.ft._distanceForTime(0, 100), 2000)

class TestPlanetSurfaceTick(unittest.TestCase):
    def setUp(self):
        self.ft = PlanetSurface("test_json/test_surfaces/full_tiling.json")

        

class TestPlanetSurfaceObjectRegionCorrespondence(unittest.TestCase):
    def setUp(self):
        self.r = 100000000000
        self.ft = PlanetSurface("test_json/test_surfaces/full_tiling.json", radius = self.r)
        self.ft.createObject(None, SurfacePoint(20, 20))
        self.ft.createObject(None, SurfacePoint(0, -10))
        self.ft.pointById(1).setDestination(SurfacePoint(0, 10))
        self.ft.pointById(1).maxV = 1

    
    def testPlanetSurfaceTickPartway(self):
        self.ft.tick(100)
        self.assertEqual(self.ft.pointById(0).point, SurfacePoint(20, 20))
        self.assertNotEqual(self.ft.pointById(1).point, SurfacePoint(0, -10))

    def testPlanetSurfaceTickMeasured(self):
        self.ft.tick((self.r*2*math.pi)/36)
        self.assertTrue(almostEqual(self.ft.pointById(1).point, SurfacePoint(0, 0)))


    def testPlanetSurfaceTickArrival(self):
        self.ft.tick(999999999999)
        self.assertEqual(self.ft.pointById(1).point, SurfacePoint(0, 10))
        self.assertIsNone(self.ft.pointById(1).destination)
