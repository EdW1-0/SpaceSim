import unittest

from colonysim import ProductionBuildingClass


class TestProductionBuildingClass(unittest.TestCase):
    def testProductionBuildingClass(self):
        self.assertTrue(ProductionBuildingClass)

    def testProductionBuildingConstructor(self):
        self.assertTrue(ProductionBuildingClass("MOCK", "Mock"))
        self.assertTrue(
            ProductionBuildingClass("MOCK", "Mock", reactions={"ELECTROLYSIS": 2.0})
        )
        self.assertTrue(
            ProductionBuildingClass(
                "MOCK", "Mock", constructionTime=50, reactions={"SABATIER": 2.0}
            )
        )
        self.assertTrue(
            ProductionBuildingClass(
                "MOCK",
                "Mock",
                constructionTime=50,
                constructionCost=30,
                reactions={"SABATIER": 2.0},
            )
        )

    def testProductionBuildingAttributes(self):
        pb = ProductionBuildingClass("MOCK", "Mock")
        self.assertTrue(hasattr(pb, "reactions"))
        self.assertTrue(isinstance(pb.reactions, dict))
