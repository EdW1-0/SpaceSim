import unittest

from colonysim.building import Building, BuildingStatus, BuildingStatusError, ProductionBuilding, StorageBuilding
from colonysim.buildingClass import BuildingClass, ProductionBuildingClass, StorageBuildingClass

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

class TestProductionBuilding(unittest.TestCase):
    def setUp(self):
        self.pbc = ProductionBuildingClass("MOCK", "Mock", reactions={"SABATIER": 2.0})

    def testProductionBuilding(self):
        self.assertTrue(ProductionBuilding)

    def testProductionBuildingConstructor(self):
        self.assertTrue(ProductionBuilding(3, self.pbc))

class TestStorageBuilding(unittest.TestCase):
    def setUp(self):
        self.sbc = StorageBuildingClass("MOCK", "Mock", stores={"O2": 1000, "H2": 8000})

    def testStorageBuilding(self):
        self.assertTrue(StorageBuilding)

    def testStorageBuildingConstructor(self):
        self.assertTrue(StorageBuilding(7, self.sbc))
        
    def testStorageBuildingAttributes(self):
        sb = StorageBuilding(5, self.sbc)
        self.assertTrue(hasattr(sb, "amount"))
        self.assertTrue(hasattr(sb, "contents"))

    def testStorageBuildingSetContents(self):
        sb = StorageBuilding(3, self.sbc)
        
        self.assertEqual(sb.contents, "O2")
        sb.setContents("H2")
        self.assertEqual(sb.contents, "H2")

        with self.assertRaises(KeyError):
            sb.setContents("CO2")

        sb.amount = 5
        with self.assertRaises(ValueError):
            sb.setContents("H2")

    def testStorageBuildingCapacity(self):
        sb = StorageBuilding(4, self.sbc)
        self.assertEqual(sb.capacity(), 1000)
        sb.setContents("H2")
        self.assertEqual(sb.capacity(), 8000)
        
    def testStorageBuildingAddMaterial(self):
        sb = StorageBuilding(6, self.sbc)
        sb.setContents("H2")
        self.assertEqual(sb.add({"H2": 6000}), 0)
        self.assertEqual(sb.amount, 6000)
        self.assertEqual(sb.add({"H2": 3000}), 1000)
        self.assertEqual(sb.amount, 8000)
        with self.assertRaises(KeyError):
            sb.add({"O2": 1000})
        with self.assertRaises(TypeError):
            sb.add(1000)
        with self.assertRaises(ValueError):
            sb.add({"H2": 100, "O2": 100})

    def testStorageBuildingRemoveMaterial(self):
        sb = StorageBuilding(8, self.sbc)
        sb.setContents("O2")
        sb.add({"O2": 1000})
        self.assertEqual(sb.remove({"O2": 200}), 200)
        self.assertEqual(sb.amount, 800)
        self.assertEqual(sb.remove({"O2": 1400}), 800)
        self.assertEqual(sb.amount, 0)

        with self.assertRaises(KeyError):
            sb.remove({"H2": 100})
        with self.assertRaises(TypeError):
            sb.remove(100)
        with self.assertRaises(ValueError):
            sb.remove({"H2": 10, "O2": 10})





        