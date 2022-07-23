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

    def testPlanetSurfaceFullTiling(self):
        self.assertEqual(self.fulltile.regionById(2).borders[2].p1, SurfacePoint(0, 240))
        self.assertEqual(self.fulltile.regionById(2).borders[2].p2, SurfacePoint(0, 120))

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

        

class TestPlanetSurfaceObjectTick(unittest.TestCase):
    def setUp(self):
        self.r = 100000000000
        self.ft = PlanetSurface("test_json/test_surfaces/full_tiling.json", radius = self.r)
        self.ft.createObject(None, SurfacePoint(20, 20))
        self.ft.createObject(None, SurfacePoint(0, -10))
        self.ft.createObject(None, SurfacePoint(0, 0))
        self.ft.pointById(2).setDestination(SurfacePoint(90, 0))
        self.ft.pointById(2).maxV = 1
        self.ft.pointById(2).fuel = 1000000000000000000
        self.ft.pointById(1).setDestination(SurfacePoint(0, 10))
        self.ft.pointById(1).maxV = 1
        self.ft.pointById(1).fuel = 1000000000000000000

    
    def testPlanetSurfaceTickPartway(self):
        self.ft.tick(100)
        self.assertEqual(self.ft.pointById(0).point, SurfacePoint(20, 20))
        self.assertNotEqual(self.ft.pointById(1).point, SurfacePoint(0, -10))

    def testPlanetSurfaceTick45(self):
        self.ft.pointById(1).setDestination(SurfacePoint(0, 30))
        self.ft.tick((self.r*2*math.pi)/36)
        self.assertAlmostEqual(self.ft.gcDistance(SurfacePath(self.ft.pointById(1).point, SurfacePoint(0, -10))),
         (self.r*2*math.pi)/36,
         places = 1)
        self.assertTrue(almostEqual(self.ft.pointById(1).point, SurfacePoint(0, 0), True))

    def testPlanetSurfaceTickQuarter(self):
        self.ft.tick((self.r*2*math.pi)/8)
        self.assertTrue(almostEqual(self.ft.pointById(2).point, SurfacePoint(45, 0)))


    def testPlanetSurfaceTickMeasured(self):
        self.ft.tick((self.r*2*math.pi)/36)
        self.assertTrue(almostEqual(self.ft.pointById(1).point, SurfacePoint(0, 0), True))
        self.assertTrue(almostEqual(self.ft.pointById(2).point, SurfacePoint(10, 0), True))


    def testPlanetSurfaceTickArrival(self):
        self.ft.tick(999999999999)
        self.assertEqual(self.ft.pointById(1).point, SurfacePoint(0, 10))
        self.assertIsNone(self.ft.pointById(1).destination)

    def testPlanetSurfaceRepeatedTicks(self):
        self.ft.tick((self.r*2*math.pi)/36)
        self.ft.tick((self.r*2*math.pi)/36)
        self.ft.tick((self.r*2*math.pi)/36)
        self.assertTrue(almostEqual(self.ft.pointById(2).point, SurfacePoint(30, 0), True))
        self.ft.pointById(2).point = SurfacePoint(0, 0)
        self.ft.tick(3*(self.r*2*math.pi)/36)
        self.assertTrue(almostEqual(self.ft.pointById(2).point, SurfacePoint(30, 0), True))

class TestPlanetSurfaceFuelConsumption(unittest.TestCase):
    def setUp(self):
        self.r = 3.6*500/math.pi
        self.ft = PlanetSurface("test_json/test_surfaces/full_tiling.json", radius = self.r)
        self.ft.createObject(None, SurfacePoint(0, 0))
        self.p1 = self.ft.pointById(0)
        self.p1.setDestination(SurfacePoint(-45, -45))
        self.p1.fuelPerM = 10.0
        self.p1.maxV = 1
        self.p1.fuel = 100

    def testFuelConsumption(self):
        self.ft.tick(3)
        self.assertEqual(self.p1.fuel, 70)

    def testFuelArrival(self):
        self.p1.setDestination(SurfacePoint(0, -5))
        self.p1.fuel = 1000
        self.ft.tick(100)
        self.assertEqual(self.p1.point, SurfacePoint(0, -5))
        self.assertEqual(self.p1.fuel, 500)

    def testFuelExhaustion(self):
        self.p1.setDestination(SurfacePoint(0, -90))
        self.ft.tick(50)
        self.assertEqual(self.p1.fuel, 0)
        self.assertEqual(self.p1.point, SurfacePoint(0, -1))

    def testFuelExhaustionOnTarget(self):
        self.p1.setDestination(SurfacePoint(0, -2))
        self.ft.tick(1000)
        self.assertEqual(self.p1.fuel, 0)
        self.assertEqual(self.p1.point, SurfacePoint(0, -1))


class TestPlanetSurfaceRegionTesting(unittest.TestCase):
    def setUp(self):
        self.r = 3.6*500/math.pi
        self.ft = PlanetSurface("test_json/test_surfaces/full_tiling.json", radius = self.r)
        self.ft.createObject(None, SurfacePoint(88, 0))
        self.ft.createObject(None, SurfacePoint(-88, 0))
        self.ft.createObject(None, SurfacePoint(10, 10))
        self.ft.createObject(None, SurfacePoint(-10, 350))

    def testRegionForPoint(self):
        self.assertEqual(self.ft.regionForPoint(self.ft.pointById(0)).id, 0)
        self.assertEqual(self.ft.regionForPoint(self.ft.pointById(1)).id, 7)
        self.assertEqual(self.ft.regionForPoint(self.ft.pointById(2)).id, 1)
        self.assertEqual(self.ft.regionForPoint(self.ft.pointById(3)).id, 6)

    def testRegionForPointOnAnchor(self):
        self.ft.createObject(None, SurfacePoint(90, 0))
        self.assertEqual(self.ft.regionForPoint(self.ft.pointById(4)).id, 0)

    @unittest.expectedFailure
    def testRegionForPointOnAnchorFPError(self):
        self.ft.createObject(None, SurfacePoint(-40, 300))
        self.assertEqual(self.ft.regionForPoint(self.ft.pointById(4)).id, 6)

    def testRegionForPointOnBorder(self):
        pass

    def testRegionForPointNotFullTiled(self):
        pass
        
        