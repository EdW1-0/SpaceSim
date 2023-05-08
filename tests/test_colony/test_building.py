import unittest

from colonysim.building import Building, BuildingStatus, BuildingStatusError
from colonysim.buildingClass import BuildingClass

class TestBuilding(unittest.TestCase):
    def setUp(self):
        self.bc = BuildingClass("MOCK", "Mock Building")

    def testBuilding(self):
        self.assertTrue(Building)

    def testBuildingConstructor(self):
        self.assertTrue(Building(1, self.bc))
        
    def testBuildingDefaults(self):
        self.assertEqual(Building(1, self.bc).condition, 100.0)
        self.assertEqual(Building(1, self.bc).status, BuildingStatus.CONSTRUCTION)

    def testBuildingAttributes(self):
        b = Building(1, self.bc)
        self.assertTrue(hasattr(b, "id"))
        self.assertTrue(hasattr(b, "buildingClass"))
        self.assertTrue(hasattr(b, "status"))
        self.assertTrue(hasattr(b, "condition"))

    def testBuildingStateMachine(self):
        b = Building(5, self.bc)
        with self.assertRaises(BuildingStatusError):
            b.start()
        with self.assertRaises(BuildingStatusError):
            b.stop()
        b.construct()
        self.assertEqual(b.status, BuildingStatus.IDLE)
        with self.assertRaises(BuildingStatusError):
            b.construct()

        b.start()
        self.assertEqual(b.status, BuildingStatus.ACTIVE)
        with self.assertRaises(BuildingStatusError):
            b.start()
        with self.assertRaises(BuildingStatusError):
            b.construct()

        b.stop()
        self.assertEqual(b.status, BuildingStatus.IDLE)
        with self.assertRaises(BuildingStatusError):
            b.stop()





        