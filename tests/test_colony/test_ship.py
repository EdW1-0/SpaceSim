import unittest

from colonysim.ship import Ship

class TestShip(unittest.TestCase):
    def testShip(self):
        self.assertTrue(Ship)

    def testShipConstructor(self):
        self.assertTrue(Ship(""))

    def testShipAttributes(self):
        self.assertTrue(hasattr(Ship("foo"), "name"))
        self.assertTrue(hasattr(Ship(""), "deltaV"))