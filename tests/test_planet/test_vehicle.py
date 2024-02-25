import unittest

from planetsim import Vehicle, VehicleClass, VehicleStatus, VehicleStatusError


class TestVehicle(unittest.TestCase):
    def setUp(self):
        self.vc = VehicleClass("BUG", "Bug", maxFuel=100, maxV=2.0, fuelPerM=1.0)

    def testVehicleClass(self):
        self.assertTrue(Vehicle)

    def testVehicleClassConstructor(self):
        self.assertTrue(Vehicle(0, "Bug 1", self.vc))
        self.assertTrue(Vehicle(0, "Bug 1", self.vc, fuel=100))
        self.assertEqual(Vehicle(0, "foo", self.vc).constructionProgress, 0)
        self.assertEqual(Vehicle(0, "foo", self.vc, constructionProgress=67).constructionProgress, 67)
        self.assertEqual(Vehicle(0, "bar", self.vc, status=VehicleStatus.IDLE).constructionProgress, 100)

    def testVehicleClassAttributes(self):
        vc = Vehicle(0, "Bug 1", self.vc)
        self.assertTrue(hasattr(vc, "id"))
        self.assertTrue(hasattr(vc, "name"))
        self.assertTrue(hasattr(vc, "vehicleClass"))
        self.assertTrue(hasattr(vc, "fuel"))
        self.assertTrue(hasattr(vc, "status"))
        self.assertTrue(hasattr(vc, "constructionProgress"))

    def testShipStateMachine(self):
        v = Vehicle(0, "Bug", self.vc)
        self.assertTrue(v.status, VehicleStatus.CONSTRUCTION)
        with self.assertRaises(VehicleStatusError):
            v.active()
        with self.assertRaises(VehicleStatusError):
            v.idle()
        
        v.construct()
        self.assertTrue(v.status, VehicleStatus.IDLE)
        with self.assertRaises(VehicleStatusError):
            v.construct()

        with self.assertRaises(VehicleStatusError):
            v.idle()

        v.active()
        self.assertTrue(v.status, VehicleStatus.ACTIVE)

        with self.assertRaises(VehicleStatusError):
            v.active()

        v.idle()
        self.assertTrue(v.status, VehicleStatus.IDLE)
        