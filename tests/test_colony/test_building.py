import unittest

from colonysim.building import (
    Building,
    BuildingStatus,
    BuildingStatusError,
    ProductionBuilding,
    StorageBuilding,
    ExtractionBuilding,
)
from colonysim.buildingClass import (
    BuildingClass,
    ProductionBuildingClass,
    StorageBuildingClass,
    ExtractionBuildingClass,
)
from colonysim.colonySim import ColonySim


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
        self.assertTrue(hasattr(b, "constructionProgress"))
        self.assertTrue(hasattr(b, "demolitionProgress"))

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

        b.demolish()
        self.assertEqual(b.status, BuildingStatus.DEMOLITION)
        with self.assertRaises(BuildingStatusError):
            b.construct()
        with self.assertRaises(BuildingStatusError):
            b.start()
        with self.assertRaises(BuildingStatusError):
            b.stop()


class TestProductionBuilding(unittest.TestCase):
    def setUp(self):
        self.pbc = ProductionBuildingClass(
            "MOCK", "Mock", reactions={"SABATIER": 2.0, "ELECTROLYSIS": 3.0}
        )
        self.cs = ColonySim()

    def testProductionBuilding(self):
        self.assertTrue(ProductionBuilding)

    def testProductionBuildingConstructor(self):
        self.assertTrue(
            ProductionBuilding(3, buildingClass=self.pbc, colonySim=self.cs)
        )

    def testProductionBuildingAttributes(self):
        pb = ProductionBuilding(6, self.pbc, self.cs)
        self.assertTrue(hasattr(pb, "reaction"))
        self.assertTrue(hasattr(pb, "rate"))

    def testProductionBuildingSetReaction(self):
        pb = ProductionBuilding(2, self.pbc, self.cs)
        self.assertEqual(pb.reaction, "SABATIER")
        pb.setReaction("ELECTROLYSIS")
        self.assertEqual(pb.reaction, "ELECTROLYSIS")
        with self.assertRaises(KeyError):
            pb.setReaction("HABER")

    def testProductionBuildingReact(self):
        pb = ProductionBuilding(4, self.pbc, self.cs)
        pb.setReaction("SABATIER")
        self.assertEqual(
            pb.react({"CO2": 20, "H2O": 20}),
            {"CO2": 18.0, "H2O": 16.0, "CH4": 2.0, "O2": 4.0},
        )

    def testProductionBuildingReactAddProducts(self):
        pb = ProductionBuilding(7, self.pbc, self.cs)
        pb.setReaction("ELECTROLYSIS")
        self.assertEqual(
            pb.react({"H2O": 20, "O2": 6, "ENERGY": 1000}),
            {"H2O": 14.0, "H2": 6.0, "O2": 9.0, "ENERGY": 700.0},
        )

    def testProductionBuildingReactPassInert(self):
        pb = ProductionBuilding(8, self.pbc, self.cs)
        pb.setReaction("SABATIER")
        self.assertEqual(
            pb.react({"CO2": 20, "H2O": 20, "Xe": 5}),
            {"CO2": 18.0, "H2O": 16.0, "CH4": 2.0, "O2": 4.0, "Xe": 5},
        )

    def testProductionBuildingReactFraction(self):
        pb = ProductionBuilding(9, self.pbc, self.cs)
        pb.setReaction("SABATIER")
        self.assertEqual(
            pb.react({"CO2": 20, "H2O": 1}),
            {"CO2": 19.5, "H2O": 0, "CH4": 0.5, "O2": 1.0},
        )
        self.assertEqual(
            pb.react({"CO2": 1, "H2O": 1}),
            {"CO2": 0.5, "H2O": 0.0, "CH4": 0.5, "O2": 1.0},
        )
        self.assertEqual(
            pb.react({"CO2": 0.0, "H2O": 300}),
            {"CO2": 0.0, "H2O": 300.0, "CH4": 0.0, "O2": 0.0},
        )

    def testProductionBuildingReactBadInput(self):
        pb = ProductionBuilding(9, self.pbc, self.cs)
        pb.setReaction("SABATIER")
        with self.assertRaises(KeyError):
            pb.react({"CO2": 1.0})
        with self.assertRaises(TypeError):
            pb.react("CO2")

    def testProductionBuildingReactQuota(self):
        pb = ProductionBuilding(10, self.pbc, self.cs)
        pb.setReaction("ELECTROLYSIS")
        self.assertEqual(
            pb.react({"ENERGY": 1000, "H2O": 20}),
            {"O2": 3.0, "H2": 6.0, "H2O": 14.0, "ENERGY": 700.0},
        )
        self.assertEqual(
            pb.react({"ENERGY": 1000, "H2O": 20}, quota=9000),
            {"O2": 3.0, "H2": 6.0, "H2O": 14.0, "ENERGY": 700.0},
        )
        self.assertEqual(
            pb.react({"ENERGY": 1000, "H2O": 20}, quota=1),
            {"O2": 1.0, "H2": 2.0, "H2O": 18.0, "ENERGY": 900.0},
        )


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


class TestExtractionBuilding(unittest.TestCase):
    def setUp(self):
        self.ebc = ExtractionBuildingClass("MOCK", "Mock", extracts={"ENERGY": 100})

    def testExtractionBuilding(self):
        self.assertTrue(ExtractionBuilding)

    def testExtractionBuildingConstructor(self):
        self.assertTrue(ExtractionBuilding(0, self.ebc))

    def testExtractionBuildingRate(self):
        eb = ExtractionBuilding(0, self.ebc)
        self.assertEqual(eb.rate(), 100)

    def testExtractBuildingExtract(self):
        eb = ExtractionBuilding(0, self.ebc)
        self.assertEqual(eb.extract(20), 20)
        self.assertEqual(eb.extract(200), 100)
        self.assertEqual(eb.extract(), 100)
        self.assertEqual(eb.extract(0), 0)
