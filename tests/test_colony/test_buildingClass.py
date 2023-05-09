import unittest

from colonysim.buildingClass import BuildingClass, StorageBuildingClass

class TestBuildingClass(unittest.TestCase):
    def testBuildingClass(self):
        self.assertTrue(BuildingClass)

    def testBuildingClassConstructor(self):
        self.assertTrue(BuildingClass("MONUMENT", "Monument"))
        self.assertTrue(BuildingClass("MONUMENT", "Monument", constructionTime = 100))
        self.assertTrue(BuildingClass("MONUMENT", "Monument", constructionTime = 100, constructionCost = {"STEEL", 50}))

    def testBuildingClassAttributes(self):
        bc = BuildingClass("BOX", "Box")
        self.assertTrue(hasattr(bc, "id"))
        self.assertTrue(hasattr(bc, "name"))
        self.assertTrue(hasattr(bc, "constructionCost"))
        self.assertTrue(hasattr(bc, "constructionTime"))
        self.assertTrue(isinstance(bc.constructionCost, dict))

class TestStorageBuildingClass(unittest.TestCase):
    def testStorageBuildingClass(self):
        self.assertTrue(StorageBuildingClass)

    def testStorageBuildingClassConstructor(self):
        self.assertTrue(StorageBuildingClass("TANK", "Gas Tank"))
        self.assertTrue(StorageBuildingClass("TANK", "Gas Tank", stores={"O2": 1000, "H2": 18000}))
        
    def testStorageBuildingClassAttributes(self):
        sbc = StorageBuildingClass("TANK", "Gas Tank")
        self.assertTrue(hasattr(sbc, "stores"))