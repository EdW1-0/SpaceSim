import unittest

from colonysim.buildingClass import BuildingClass

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
        