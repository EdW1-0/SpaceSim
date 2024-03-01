import unittest

from peoplesim.peopleSim import PeopleSim

class TestPeopleSim(unittest.TestCase):
    def testPeopleSim(self):
        self.assertTrue(PeopleSim)
        self.assertTrue(PeopleSim())

    def testPeopleSimConstructor(self):
        self.assertTrue(PeopleSim(jsonPath="test_json/test_people"))

    def testPeopleSimAttributes(self):
        self.assertTrue(hasattr(PeopleSim(), "_people"))