import unittest

from colonysim.ship import Ship
from colonysim.shipClass import ShipClass

class TestShip(unittest.TestCase):
    def setUp(self):
        self.sc = ShipClass("TEST", "Test", 100)

    def testShip(self):
        self.assertTrue(Ship)

    def testShipConstructor(self):
        self.assertTrue(Ship(0, "Ship 0", self.sc))

    def testShipAttributes(self):
        s = Ship(0, "Ship 1", self.sc)
        self.assertTrue(hasattr(s, "id"))
        self.assertTrue(hasattr(s, "name"))
        self.assertTrue(hasattr(s, "deltaV"))
        self.assertTrue(hasattr(s, "shipClass"))