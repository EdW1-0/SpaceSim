import unittest

from colonysim.building import Building, BuildingStatus

class TestBuilding(unittest.TestCase):
    def testBuilding(self):
        self.assertTrue(Building)

    def testBuildingConstructor(self):
        self.assertTrue(Building(1, "MONUMENT"))
        
    def testBuildingDefaults(self):
        self.assertEqual(Building(1, "MONUMENT").condition, 100.0)
        self.assertEqual(Building(1, "MONUMENT").status, BuildingStatus.CONSTRUCTION)

    def testBuildingAttributes(self):
        b = Building(1, "MONUMENT")
        self.assertTrue(hasattr(b, "id"))
        self.assertTrue(hasattr(b, "buildingClass"))
        self.assertTrue(hasattr(b, "status"))
        self.assertTrue(hasattr(b, "condition"))
        