import unittest

from colonysim import (
    BuildingClass,
    StorageBuildingClass,
    ExtractionBuildingClass,
)

from techtree import PlayerTech, TechEffectParameter


class TestBuildingClass(unittest.TestCase):
    def testBuildingClass(self):
        self.assertTrue(BuildingClass)

    def testBuildingClassConstructor(self):
        self.assertTrue(BuildingClass("MONUMENT", "Monument", "MARTIAN"))
        self.assertTrue(BuildingClass("MONUMENT", "Monument", "MARTIAN", constructionTime=100))
        self.assertTrue(
            BuildingClass(
                "MONUMENT",
                "Monument",
                "MARTIAN", 
                constructionTime=100,
                constructionCost={"STEEL", 50},
            )
        )
        self.assertTrue(BuildingClass("MONUMENT", "Monument", "MARTIAN", demolitionTime=20))
        self.assertTrue(
            BuildingClass(
                "MONUMENT", "Monument", "MARTIAN", demolitionTime=20, demolitionCost={"ENERGY": 20}
            )
        )

    def testBuildingClassAttributes(self):
        bc = BuildingClass("BOX", "Box", "MARTIAN", playerTech=PlayerTech())
        self.assertTrue(hasattr(bc, "id"))
        self.assertTrue(hasattr(bc, "name"))
        self.assertTrue(hasattr(bc, "environId"))
        self.assertTrue(hasattr(bc, "baseConstructionCost"))
        self.assertTrue(hasattr(bc, "baseConstructionTime"))
        self.assertTrue(hasattr(bc, "demolitionTime"))
        self.assertTrue(hasattr(bc, "demolitionCost"))
        self.assertTrue(isinstance(bc.baseConstructionCost, dict))


class TestStorageBuildingClass(unittest.TestCase):
    def testStorageBuildingClass(self):
        self.assertTrue(StorageBuildingClass)

    def testStorageBuildingClassConstructor(self):
        self.assertTrue(StorageBuildingClass("TANK", "Gas Tank", "MARTIAN"))
        self.assertTrue(
            StorageBuildingClass("TANK", "Gas Tank", "MARTIAN", stores={"O2": 1000, "H2": 18000})
        )

    def testStorageBuildingClassAttributes(self):
        sbc = StorageBuildingClass("TANK", "Gas Tank", "MARTIAN")
        self.assertTrue(hasattr(sbc, "stores"))


class TestExtractionBuildingClass(unittest.TestCase):
    def testExtractionBuildingClass(self):
        self.assertTrue(ExtractionBuildingClass)

    def testExtractionBuildingClassConstructor(self):
        self.assertTrue(ExtractionBuildingClass("SOLAR", "Solar Array", "MARTIAN"))
        self.assertTrue(
            ExtractionBuildingClass("SOLAR", "Solar Array", "MARTIAN", extracts={"ENERGY": 100})
        )

    def testExtractionBuildingClassAttributes(self):
        ebc = ExtractionBuildingClass("FOO", "Bar", "MARTIAN")
        self.assertTrue(hasattr(ebc, "extracts"))

class TestBuildingClassParameters(unittest.TestCase):
    def setUp(self):
        self.pt = PlayerTech()
        self.bc = BuildingClass(0, "Test", "MARTIAN", self.pt)

    def testBuildingClassConstructionTime(self):
        self.assertEqual(self.bc.constructionTime(), 10)
        te = TechEffectParameter("MARTIAN_CONSTRUCTION_SPEED", 1)
        self.pt._processEffects([te])
        self.assertEqual(self.bc.constructionTime(), 5)
        self.pt._processEffects([TechEffectParameter("MARTIAN_CONSTRUCTION_SPEED", 8)])
        self.assertEqual(self.bc.constructionTime(), 1)

        # self.pt._processEffects([TechEffectParameter("ORBITAL_CONSTRUCTION_SPEED", 5)])
        # self.assertEqual(self.bc.constructionTime(), 1)


