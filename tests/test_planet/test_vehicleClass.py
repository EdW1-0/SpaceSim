import unittest

from planetsim import VehicleClass
from playerState import PlayerState

class TestVehicleClass(unittest.TestCase):
    def testVehicleClass(self):
        self.assertTrue(VehicleClass)

    def testVehicleClassConstructor(self):
        self.assertTrue(VehicleClass("ROVER", "Rover"))
        self.assertTrue(VehicleClass("ROVER", "Rover", maxFuel=1000))
        self.assertTrue(VehicleClass("ROVER", "Rover", maxFuel=1000, maxV=2.0))
        self.assertTrue(VehicleClass("ROVER", "Rover", maxFuel=1000, fuelPerM=5.0))
        self.assertTrue(VehicleClass("ROVER", "Rover", maxFuel=1000, maxV=2.0, fuelPerM=5.0, constructionTime=100, constructionCost={"AL": 100}))

    def testVehicleClassAttributes(self):
        vc = VehicleClass("ROVER", "Rover")
        self.assertTrue(hasattr(vc, "id"))
        self.assertTrue(hasattr(vc, "name"))
        self.assertTrue(hasattr(vc, "maxV"))
        self.assertTrue(hasattr(vc, "maxFuel"))
        self.assertTrue(hasattr(vc, "fuelPerM"))
        self.assertTrue(hasattr(vc, "baseConstructionCost"))
        self.assertTrue(hasattr(vc, "baseConstructionTime"))

class TestVehicleClassParameters(unittest.TestCase):
    def setUp(self):
        self.ps = PlayerState()
        self.vc = VehicleClass("ROVER", 
                               "Rover", 
                               playerState=self.ps, 
                               maxFuel=1000, 
                               maxV=2.0, 
                               fuelPerM=5.0, 
                               constructionCost={"AL": 10}, 
                               constructionTime=100)

    def testVehicleClassConstructionParams(self):
        self.assertEqual(self.vc.maxV, 2.0)
        self.assertEqual(self.vc.maxFuel, 1000)
        self.assertEqual(self.vc.fuelPerM, 5.0)
        self.assertEqual(self.vc.constructionTime(), 100)
        self.assertEqual(self.vc.constructionCost(), {"AL": 10})
