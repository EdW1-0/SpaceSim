import unittest

from playerState import PlayerState

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



class TestPlayerStateBuildingParams(unittest.TestCase):
    def setUp(self):
        self.ps = PlayerState()

    def testPlayerStateConstructionTime(self):
        self.assertTrue(self.ps.constructionTime(id, 100))