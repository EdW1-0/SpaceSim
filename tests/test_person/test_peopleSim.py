import unittest

from peoplesim.peopleSim import PeopleSim

class TestPeopleSim(unittest.TestCase):
    def testPeopleSim(self):
        self.assertTrue(PeopleSim)
        self.assertTrue(PeopleSim())