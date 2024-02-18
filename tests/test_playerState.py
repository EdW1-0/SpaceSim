import unittest

from playerState import PlayerState
from colonysim import BuildingClass

class TestPlayerState(unittest.TestCase):
    def testPlayerState(self):
        self.assertTrue(PlayerState)

    def testPlayerStateConstructor(self):
        self.assertTrue(PlayerState())

    def testPlayerStateAttributes(self):
        ps = PlayerState()
        self.assertTrue(hasattr(ps, "_parameters"))

class TestPlayerStateLoading(unittest.TestCase):
    def testPlayerStateLoading(self):
        ps = PlayerState(filePath = "test_json/test_parameters.json")

        self.assertEqual(len(ps._parameters), 3)

        self.assertEqual(ps._parameters["TEST_PARAMETER_1"], [1.0])

class TestPlayerStateResearchEffects(unittest.TestCase):
    def setUp(self):
        self.ps = PlayerState(filePath = "test_json/test_parameters.json")

    def testPlayerStateResearchTech(self):

        self.ps.applyModifier("TEST_PARAMETER_1", 0.1)

        self.assertEqual(self.ps._parameters["TEST_PARAMETER_1"], [1.0, 0.1])

    def testPlayerStateResearchTechMultiple(self):

        self.ps.applyModifier("TEST_PARAMETER_3", 0.1)
        self.ps.applyModifier("TEST_PARAMETER_3", 0.7)
        self.ps.applyModifier("TEST_PARAMETER_3", -0.1)
        self.assertEqual(self.ps._parameters["TEST_PARAMETER_3"], [1.0, 0.1, 0.7, -0.1])

    def testPlayerStateReseachTechNonExistant(self):
        with self.assertRaises(KeyError):
            self.ps.applyModifier("TEST_PARAMETER_NONE", 0.1)

class TestPlayerStateParamArithmetic(unittest.TestCase):
    def setUp(self):
        self.ps = PlayerState(filePath = "test_json/test_parameters.json")

    def testPlayerStateParamSum(self):
        self.ps.applyModifier("TEST_PARAMETER_1", 0.1)
        self.ps.applyModifier("TEST_PARAMETER_1", 0.4)
        self.ps.applyModifier("TEST_PARAMETER_1", -0.2)

        self.assertEqual(self.ps._paramSum("TEST_PARAMETER_1"), 1.3)

class TestPlayerStateBuildingParams(unittest.TestCase):
    def setUp(self):
        self.ps = PlayerState()
        self.bc = BuildingClass("ROB_FAC", "robot factory", "MARTIAN")
        self.oc = BuildingClass("HAB_MOD", "Hab mod", "ORBITAL")
        self.ac = BuildingClass("HEL_CON", "Helium condensor", "AEROSTAT")
        self.pc = BuildingClass("FUS_REA", "Fusion reactor", "PLUTONIC")
        self.rc = BuildingClass("NEX_SPL", "Nexus splicer", "UNDEFINED")

    def testPlayerStateBaseConstructionTime(self):
        self.assertEqual(self.ps.constructionTime(self.bc.environId, 100), 100)

    def testPlayerStateGenConstructionTime(self):
        self.ps.applyModifier("GENERAL_CONSTRUCTION_SPEED", 1.0)

        self.assertEqual(self.ps.constructionTime(self.bc.environId, 100), 50)

    def testPlayerStateMartianConstructionTime(self):

        self.assertEqual(self.ps.constructionTime(self.bc.environId, 100), 100)

        self.ps.applyModifier("MARTIAN_CONSTRUCTION_SPEED", 1.0)

        self.assertEqual(self.ps.constructionTime(self.bc.environId, 100), 50)
    
    def testPlayerStateOrbitalConstructionTime(self):
        
        self.ps.applyModifier("ORBITAL_CONSTRUCTION_SPEED", 3.0)

        self.assertEqual(self.ps.constructionTime(self.oc.environId, 100), 25)

    def testPlayerStateAerosatConstructionTime(self):
        
        self.ps.applyModifier("AEROSTAT_CONSTRUCTION_SPEED", 3.0)

        self.assertEqual(self.ps.constructionTime(self.ac.environId, 100), 25)

    def testPlayerStatePlutonicConstructionTime(self):
        
        self.ps.applyModifier("PLUTONIC_CONSTRUCTION_SPEED", 3.0)

        self.assertEqual(self.ps.constructionTime(self.pc.environId, 100), 25)

    def testPlayerStateUndefinedConstructionTime(self):

        self.assertEqual(self.ps.constructionTime(self.rc.environId, 100), 100)

    def testPlayerStateConstructionTimeCrosstalk(self):
        self.ps.applyModifier("GENERAL_CONSTRUCTION_SPEED", 1.0)
        self.ps.applyModifier("ORBITAL_CONSTRUCTION_SPEED", 1.0)
        self.ps.applyModifier("MARTIAN_CONSTRUCTION_SPEED", 4.0)
        self.ps.applyModifier("AEROSTAT_CONSTRUCTION_SPEED", 9.0)

        self.assertEqual(self.ps.constructionTime(self.bc.environId, 100), 10)
        self.assertEqual(self.ps.constructionTime(self.oc.environId, 100), 25)
        self.assertEqual(self.ps.constructionTime(self.ac.environId, 100), 5)
        self.assertEqual(self.ps.constructionTime(self.pc.environId, 100), 50)
        self.assertEqual(self.ps.constructionTime(self.rc.environId, 100), 50)

    def testPlayerStateBaseConstructionCost(self):
        self.assertEqual(self.ps.constructionCost(self.bc.environId, {"ENERGY": 100, "AL": 50}), {"ENERGY": 100, "AL": 50})

    def testPlayerStateGenConstructionCost(self):
        self.ps.applyModifier("GENERAL_CONSTRUCTION_COST_MODIFIER", 1.0)
        self.assertEqual(self.ps.constructionCost(self.bc.environId, {"ENERGY": 100, "AL": 50}), {"ENERGY": 50, "AL": 25})

    def testPlayerStateEnvironConstructionCost(self):
        baseCC = {"ENERGY": 100, "AL": 50}
        self.ps.applyModifier("ORBITAL_CONSTRUCTION_COST_MODIFIER", 1.0)
        self.ps.applyModifier("MARTIAN_CONSTRUCTION_COST_MODIFIER", 2.0)
        self.ps.applyModifier("AEROSTAT_CONSTRUCTION_COST_MODIFIER", 4.0)
        self.ps.applyModifier("PLUTONIC_CONSTRUCTION_COST_MODIFIER", 8.0)

        self.assertEqual(self.ps.constructionCost(self.rc.environId, baseCC), baseCC)
        self.assertEqual(self.ps.constructionCost(self.oc.environId, baseCC), {k: baseCC[k]/2.0 for k in baseCC})
        self.assertEqual(self.ps.constructionCost(self.bc.environId, baseCC), {k: baseCC[k]/3.0 for k in baseCC})
        self.assertEqual(self.ps.constructionCost(self.ac.environId, baseCC), {k: baseCC[k]/5.0 for k in baseCC})
        self.assertEqual(self.ps.constructionCost(self.pc.environId, baseCC), {k: baseCC[k]/9.0 for k in baseCC})

    def testPlayerStateShipConstructionTime(self):
        self.assertTrue(self.ps.shipConstructionTime(100), 100)
    
