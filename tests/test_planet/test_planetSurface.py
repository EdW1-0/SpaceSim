import unittest
from unittest.mock import MagicMock

import math

from planetsim.planetSurface import PlanetSurface, EARTH_RADIUS
from planetsim.surfacePath import SurfacePath
from planetsim.surfacePoint import SurfacePoint, almostEqual
from planetsim.vehicle import Vehicle
from planetsim.vehicleClass import VehicleClass
from planetsim.surfaceVehicle import SurfaceVehicle
from planetsim.planetSim import PlanetSim

class TestPlanetSurface(unittest.TestCase):
    def testPlanetSurfaceModule(self):
        self.assertTrue(PlanetSurface)
        self.assertTrue(PlanetSurface())

    def testPlanetSurfaceAttributes(self):
        self.assertTrue(hasattr(PlanetSurface(), "regions"))
        self.assertTrue(hasattr(PlanetSurface(), "points"))
        self.assertTrue(hasattr(PlanetSurface(), "radius"))
        self.assertTrue(hasattr(PlanetSurface(), "planetClass"))
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
        self.ps = PlanetSurface("test_json/test_surfaces/single_region.json", vehiclePath=None)
        self.twor = PlanetSurface("test_json/test_surfaces/2_hemispheres.json", vehiclePath=None)
        



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
        pt = self.ft.pointById(0)
        self.ft.destroyObject(0)
        self.assertEqual(len(self.ft.points), 0)
        self.assertTrue(pt.killed)

    def testSurfaceVehicleCreation(self):
        self.ft.createVehicle(None, SurfacePoint(20, 20))
        self.assertEqual(len(self.ft.points), 1)

    def testSurfaceVehicleDestruction(self):
        self.ft.createVehicle(None, SurfacePoint(20, 20))
        self.assertEqual(len(self.ft.points), 1)
        self.ft.destroyObject(0)
        self.assertEqual(len(self.ft.points), 0)


class TestPlanetSurfaceObjectMovement(unittest.TestCase):
    def setUp(self):
        self.ft = PlanetSurface("test_json/test_surfaces/full_tiling.json")
        vc = VehicleClass("ROVER", "Rover", 100, 3.0, 10.0)
        self.v = Vehicle(0, "Vic 1", vc, 100)
        self.ft.createVehicle(None, SurfacePoint(20,20), payload=self.v)
        self.pt = self.ft.pointById(0)
        


    def testSurfaceVehicleNilMovement(self):
        self.pt.setDestination(SurfacePoint(80, 100))
        self.pt.payload.vehicleClass.maxV = 0
        self.assertEqual(self.ft._distanceForTime(0, 100), 0)

    def testSurfaceVehicleFiniteMovement(self):
        self.pt.payload.vehicleClass.maxV = 20
        self.assertEqual(self.ft._distanceForTime(0, 100), 2000)

class TestPlanetSurfaceTick(unittest.TestCase):
    def setUp(self):
        self.ft = PlanetSurface("test_json/test_surfaces/full_tiling.json")

        

class TestPlanetSurfaceObjectTick(unittest.TestCase):
    def setUp(self):
        self.r = 100000000000
        vc = VehicleClass("A", "a", maxFuel = 10000000000000000, maxV = 1)
        self.ft = PlanetSurface("test_json/test_surfaces/full_tiling.json", radius = self.r)
        self.ft.createVehicle(None, SurfacePoint(20, 20), payload = Vehicle(0, "Vic 1", vc, 100000000000))
        self.ft.createVehicle(None, SurfacePoint(0, -10), payload = Vehicle(1, "Vic 2", vc, 100000000000))
        self.ft.createVehicle(None, SurfacePoint(0, 0), payload = Vehicle(2, "Vic 3", vc, 100000000000))
        self.ft.pointById(2).setDestination(SurfacePoint(90, 0))
        self.ft.pointById(1).setDestination(SurfacePoint(0, 10))

    
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
        vc = VehicleClass("A", "a", maxFuel = 10000000000000000, maxV = 1, fuelPerM=10.0)
        self.ft.createVehicle(None, SurfacePoint(0, 0), payload = Vehicle(0, "V", vc, 100))
        self.p1 = self.ft.pointById(0)
        self.p1.setDestination(SurfacePoint(-45, -45))

    def testFuelConsumption(self):
        self.ft.tick(3)
        self.assertEqual(self.p1.fuel(), 70)

    def testFuelArrival(self):
        self.p1.setDestination(SurfacePoint(0, 355))
        self.p1.payload.fuel = 1000
        self.ft.tick(100)
        self.assertEqual(self.p1.point, SurfacePoint(0, 355))
        self.assertAlmostEqual(self.p1.fuel(), 500)

    def testFuelExhaustion(self):
        self.p1.setDestination(SurfacePoint(0, 270))
        self.ft.tick(50)
        self.assertEqual(self.p1.fuel(), 0)
        self.assertEqual(self.p1.point, SurfacePoint(0, 359))

    def testFuelExhaustionOnTarget(self):
        self.p1.setDestination(SurfacePoint(0, -2))
        self.ft.tick(1000)
        self.assertEqual(self.p1.fuel(), 0)
        self.assertEqual(self.p1.point, SurfacePoint(0, 359))

    def testUnlimitedFuel(self):
        self.p1.payload.vehicleClass.fuelPerM = 0
        self.ft.tick(1000)
        self.assertEqual(self.p1.point, SurfacePoint(-45, 315))
        self.assertEqual(self.p1.fuel(), 100)

    def testIgnoresFuelIfUnlimited(self):
        self.p1.payload.vehicleClass.fuelPerM = 0
        self.p1.payload.fuel = 0
        self.ft.tick(1000)
        self.assertEqual(self.p1.point, SurfacePoint(-45, 315))
        self.assertEqual(self.p1.fuel(), 0)

class MockDestination:
    pass

class TestPlanetSurfacePointArrival(unittest.TestCase):
    def setUp(self):
        terminal = MockDestination()
        terminal.vehicleArrival = MagicMock(return_value=True)
        waypoint = MockDestination()
        waypoint.vehicleArrival = MagicMock(return_value=False)
        self.r = 3.6*500/math.pi
        self.ft = PlanetSurface("test_json/test_surfaces/full_tiling.json", radius = self.r)
        vc = VehicleClass("A", "a", maxFuel = 1000, maxV = 1)
        self.ft.createObject(terminal, SurfacePoint(10, 20))
        self.ft.createObject(waypoint, SurfacePoint(-20, 345))
        self.ft.createVehicle(None, SurfacePoint(0, 0), payload=Vehicle(0, "A", vc, 1000))
        self.p = self.ft.pointById(2)
        self.waypoint = waypoint
        self.terminal = terminal

    def testPlanetSurfaceArrivalAtWaypoint(self):
        self.ft.createVehicle(None, SurfacePoint(-5, 355))
        self.ft.pointById(2).setDestination(SurfacePoint(-20, 345))
        self.ft.tick(1000)
        self.assertIsNotNone(self.ft.pointById(2))
        self.assertIsNone(self.p.destination)
        self.assertTrue(self.waypoint.vehicleArrival.called)

    def testPlanetSurfaceArrivalAtTerminal(self):
        self.ft.createObject(None, SurfacePoint(-5, 355))
        self.ft.pointById(2).setDestination(SurfacePoint(10, 20))
        self.ft.tick(1000)
        with self.assertRaises(KeyError):
            self.ft.pointById(2)
        self.assertTrue(self.terminal.vehicleArrival.called)


    
class TestPlanetSurfaceObjectAtPoint(unittest.TestCase):
    def setUp(self):
        self.r = 3.6*500/math.pi
        self.ft = PlanetSurface("test_json/test_surfaces/full_tiling.json", radius = self.r)
        self.ft.createObject(None, SurfacePoint(50, 40))
        self.ft.createObject(None, SurfacePoint(-30, 300))
        self.ft.createObject(None, SurfacePoint(-30, 300))
        self.ft.createObject(None, SurfacePoint(-30, 300))
    
    def testObjectAtPointSingle(self):
        self.assertEqual(self.ft.objectsAtPoint(SurfacePoint(50, 40))[0].id, 0)

    def testObjectAtPointNothing(self):
        self.assertFalse(self.ft.objectsAtPoint(SurfacePoint(90, 0)))

    def testObjectAtPointClose(self):
        self.assertFalse(self.ft.objectsAtPoint(SurfacePoint(50.1, 40)))
    
    def testObjectAtPointMultiple(self):
        ps = self.ft.objectsAtPoint(SurfacePoint(-30,300))
        self.assertEqual(len(ps), 3)
        for i in range(3):
            self.assertEqual(ps[i].id, i+1)




class TestPlanetSurfaceRegionTesting(unittest.TestCase):
    def setUp(self):
        self.r = 3.6*500/math.pi
        self.ft = PlanetSurface("test_json/test_surfaces/full_tiling.json", radius = self.r)
        self.ft.createObject(None, SurfacePoint(88, 0))
        self.ft.createObject(None, SurfacePoint(-88, 0))
        self.ft.createObject(None, SurfacePoint(10, 10))
        self.ft.createObject(None, SurfacePoint(-10, 350))

    def testRegionForPoint(self):
        self.assertEqual(self.ft.regionForObject(self.ft.pointById(0)).id, 0)
        self.assertEqual(self.ft.regionForObject(self.ft.pointById(1)).id, 7)
        self.assertEqual(self.ft.regionForObject(self.ft.pointById(2)).id, 1)
        self.assertEqual(self.ft.regionForObject(self.ft.pointById(3)).id, 6)

    def testRegionForPointOnAnchor(self):
        self.ft.createObject(None, SurfacePoint(90, 0))
        self.assertEqual(self.ft.regionForObject(self.ft.pointById(4)).id, 0)

    @unittest.expectedFailure
    def testRegionForPointOnAnchorFPError(self):
        self.ft.createObject(None, SurfacePoint(-40, 300))
        self.assertEqual(self.ft.regionForPointId(self.ft.pointById(4)).id, 6)

    @unittest.skip("Skip full testing of regionForPoint as may require rework")
    def testRegionForPointOnBorder(self):
        self.assertTrue(False)

    @unittest.skip("Skip full testing of regionForPoint as may require rework")
    def testRegionForPointNotFullTiled(self):
        self.assertTrue(False)
        
class ColonyMock:
    def __init__(self, *args, **kwargs):
        self.id = 0

    def vehicleArrival(self, vehicle):
        return True

class TestPlanetSurfaceBuildColony(unittest.TestCase):
    def setUp(self):
        self.r = 3.6*500/math.pi
        self.ft = PlanetSurface("test_json/test_surfaces/full_tiling.json", radius = self.r)
        self.vehicle = Vehicle(0, VehicleClass("TEST", "Test", 100, 100, 1), 100)
        self.v = self.ft.createVehicle(content=None, position = SurfacePoint(10, 10), name = "TestVehice", payload = self.vehicle)

        

    def mockColonySimCallback(self, name, locale):
        self.calledCallback = True
        return ColonyMock()

        
    def testPlanetSurfaceBuildColony(self):
        self.calledCallback = False

        self.ft.buildColony(self.v, self.mockColonySimCallback)
        self.assertTrue(self.calledCallback)