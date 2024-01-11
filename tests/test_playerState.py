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

class TestPlayerStateBuildingParams(unittest.TestCase):
    def setUp(self):
        self.ps = PlayerState()

    def testPlayerStateConstructionTime(self):
        self.assertTrue(self.ps.constructionTime(id, 100))