import unittest

from colonysim.colony import Colony
from colonysim.buildingClass import BuildingClass
from colonysim.building import Building, BuildingStatus

class TestColony(unittest.TestCase):
    def testColony(self):
        self.assertTrue(Colony)

    def testColonyConstructor(self):
        self.assertTrue(Colony(0, "Discovery Base"))

    def testColonyAttributes(self):
        c = Colony(0, "Default")
        self.assertTrue(hasattr(c, "id"))
        self.assertTrue(hasattr(c, "name"))
        self.assertTrue(hasattr(c, "buildings"))
        self.assertTrue(isinstance(c.buildings, dict))
        self.assertTrue(hasattr(c, "ships"))
        self.assertTrue(isinstance(c.ships, dict))
        self.assertTrue(hasattr(c, "vehicles"))
        self.assertTrue(isinstance(c.vehicles, dict))

class TestColonyBuildingConstruction(unittest.TestCase):
    def setUp(self):
        self.bc = BuildingClass("MOCK", "Mock Building")

    def testColonyAddBuilding(self):
        c = Colony(0, "Default")
        self.assertEqual(c.addBuilding(self.bc), 0)
        self.assertEqual(len(c.buildings), 1)
        self.assertEqual(c.addBuilding(self.bc), 1)
        self.assertEqual(len(c.buildings), 2)

    def testColonyConstructBuilding(self):
        c = Colony(0, "Default")
        id = c.addBuilding(self.bc)
        c.constructBuilding(id)
        self.assertEqual(c.buildingById(id).status, BuildingStatus.IDLE)