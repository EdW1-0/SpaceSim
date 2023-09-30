import unittest

from planetsim.vehicle import Vehicle
from planetsim.vehicleClass import VehicleClass


class TestVehicle(unittest.TestCase):
    def setUp(self):
        self.vc = VehicleClass("BUG", "Bug", maxFuel=100, maxV=2.0, fuelPerM=1.0)

    def testVehicleClass(self):
        self.assertTrue(Vehicle)

    def testVehicleClassConstructor(self):
        self.assertTrue(Vehicle(0, "Bug 1", self.vc))
        self.assertTrue(Vehicle(0, "Bug 1", self.vc, fuel=100))

    def testVehicleClassAttributes(self):
        vc = Vehicle(0, "Bug 1", self.vc)
        self.assertTrue(hasattr(vc, "id"))
        self.assertTrue(hasattr(vc, "name"))
        self.assertTrue(hasattr(vc, "vehicleClass"))
        self.assertTrue(hasattr(vc, "fuel"))
