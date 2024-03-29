import unittest

from colonysim import (
    BuildingClass,
    StorageBuildingClass,
    ExtractionBuildingClass,
    ResearchBuildingClass
)

from techtree import PlayerTech, TechEffectParameter
from playerState import PlayerState


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
        bc = BuildingClass("BOX", "Box", "MARTIAN", playerState=PlayerState())
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

class TestReseachBuildingClass(unittest.TestCase):
    def testResearchBuildingClass(self):
        self.assertTrue(ResearchBuildingClass)

    def testResearchBuildingClassConstructor(self):
        self.assertTrue(ResearchBuildingClass("MOONLAB", "Lunar Laboratory", "MARTIAN"))
        self.assertTrue(ResearchBuildingClass("BIOLAB", "Biolaboratory", "ORBITAL", researchOutput=20))
        self.assertTrue(ResearchBuildingClass("OBSERVATORY", "Observatory", "MARTIAN", researchOutput=10, researchCallback=self.rbcCallback))

    def testResearchBuildingClassAttributes(self):
        rbc = ResearchBuildingClass("RESEARCHREACTOR", "Research Reactor", "PLUTONIC")
        self.assertTrue(hasattr(rbc, "researchOutput"))
        self.assertTrue(hasattr(rbc, "researchCallback"))

    def rbcCallback(self):
        pass    

class TestBuildingClassParameters(unittest.TestCase):
    def setUp(self):
        self.pt = PlayerTech()
        self.ps = PlayerState()
        self.pt.parameterModifierCallback = self.ps.applyModifier
        self.bc = BuildingClass(0, "Test", "MARTIAN", self.ps)

    def testBuildingClassConstructionTime(self):
        self.assertEqual(self.bc.constructionTime(), 10)
        te = TechEffectParameter("MARTIAN_CONSTRUCTION_SPEED", 1)
        self.pt._processEffects([te])
        self.assertEqual(self.bc.constructionTime(), 5)
        self.pt._processEffects([TechEffectParameter("MARTIAN_CONSTRUCTION_SPEED", 8)])
        self.assertEqual(self.bc.constructionTime(), 1)

        # self.pt._processEffects([TechEffectParameter("ORBITAL_CONSTRUCTION_SPEED", 5)])
        # self.assertEqual(self.bc.constructionTime(), 1)


