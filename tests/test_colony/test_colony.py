import unittest

from colonysim.colony import Colony

class TestColony(unittest.TestCase):
    def testColony(self):
        self.assertTrue(Colony)

    def testColonyConstructor(self):
        self.assertTrue(Colony(0, "Discovery Base"))

    def testColonyAttributes(self):
        c = Colony(0, "Default")
        self.assertTrue(hasattr(c, "id"))
        self.assertTrue(hasattr(c, "name"))
        self.assertTrue(hasattr(c, "buildings"))
        self.assertTrue(isinstance(c.buildings, dict))
        self.assertTrue(hasattr(c, "ships"))
        self.assertTrue(isinstance(c.ships, dict))
        self.assertTrue(hasattr(c, "vehicles"))
        self.assertTrue(isinstance(c.vehicles, dict))
