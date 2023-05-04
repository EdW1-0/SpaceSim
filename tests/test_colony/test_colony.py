import unittest

from colonysim.colony import Colony

class TestColony(unittest.TestCase):
    def testColony(self):
        self.assertTrue(Colony)

    def testColonyConstructor(self):
        self.assertTrue(Colony())

    def testColonyAttributes(self):
        self.assertTrue(hasattr(Colony(), "buildings"))
