import unittest

from colonysim.buildingClass import (
    BuildingClass,
    StorageBuildingClass,
    ExtractionBuildingClass,
)


class TestBuildingClass(unittest.TestCase):
    def testBuildingClass(self):
        self.assertTrue(BuildingClass)

    def testBuildingClassConstructor(self):
        self.assertTrue(BuildingClass("MONUMENT", "Monument"))
        self.assertTrue(BuildingClass("MONUMENT", "Monument", constructionTime=100))
        self.assertTrue(
            BuildingClass(
                "MONUMENT",
                "Monument",
                constructionTime=100,
                constructionCost={"STEEL", 50},
            )
        )
        self.assertTrue(BuildingClass("MONUMENT", "Monument", demolitionTime=20))
        self.assertTrue(
            BuildingClass(
                "MONUMENT", "Monument", demolitionTime=20, demolitionCost={"ENERGY": 20}
            )
        )

    def testBuildingClassAttributes(self):
        bc = BuildingClass("BOX", "Box")
        self.assertTrue(hasattr(bc, "id"))
        self.assertTrue(hasattr(bc, "name"))
        self.assertTrue(hasattr(bc, "constructionCost"))
        self.assertTrue(hasattr(bc, "constructionTime"))
        self.assertTrue(hasattr(bc, "demolitionTime"))
        self.assertTrue(hasattr(bc, "demolitionCost"))
        self.assertTrue(isinstance(bc.constructionCost, dict))


class TestStorageBuildingClass(unittest.TestCase):
    def testStorageBuildingClass(self):
        self.assertTrue(StorageBuildingClass)

    def testStorageBuildingClassConstructor(self):
        self.assertTrue(StorageBuildingClass("TANK", "Gas Tank"))
        self.assertTrue(
            StorageBuildingClass("TANK", "Gas Tank", stores={"O2": 1000, "H2": 18000})
        )

    def testStorageBuildingClassAttributes(self):
        sbc = StorageBuildingClass("TANK", "Gas Tank")
        self.assertTrue(hasattr(sbc, "stores"))


class TestExtractionBuildingClass(unittest.TestCase):
    def testExtractionBuildingClass(self):
        self.assertTrue(ExtractionBuildingClass)

    def testExtractionBuildingClassConstructor(self):
        self.assertTrue(ExtractionBuildingClass("SOLAR", "Solar Array"))
        self.assertTrue(
            ExtractionBuildingClass("SOLAR", "Solar Array", extracts={"ENERGY": 100})
        )

    def testExtractionBuildingClassAttributes(self):
        ebc = ExtractionBuildingClass("FOO", "Bar")
        self.assertTrue(hasattr(ebc, "extracts"))
