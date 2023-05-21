import unittest

from planetsim.vehicleClass import VehicleClass

class TestVehicleClass(unittest.TestCase):
    def testVehicleClass(self):
        self.assertTrue(VehicleClass)

    def testVehicleClassConstructor(self):
        self.assertTrue(VehicleClass("ROVER", "Rover"))
        self.assertTrue(VehicleClass("ROVER", "Rover", maxFuel = 1000))
        self.assertTrue(VehicleClass("ROVER", "Rover", maxFuel = 1000, maxV = 2.0))
        self.assertTrue(VehicleClass("ROVER", "Rover", maxFuel = 1000, fuelPerM=5.0))

    def testVehicleClassAttributes(self):
        vc = VehicleClass("ROVER", "Rover")
        self.assertTrue(hasattr(vc, "id"))
        self.assertTrue(hasattr(vc, "name"))
        self.assertTrue(hasattr(vc, "maxV"))
        self.assertTrue(hasattr(vc, "maxFuel"))
        self.assertTrue(hasattr(vc, "fuelPerM"))
        