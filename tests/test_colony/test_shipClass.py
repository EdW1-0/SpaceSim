import unittest

from colonysim import ShipClass


class TestShipClass(unittest.TestCase):
    def testShipClass(self):
        self.assertTrue(ShipClass)

    def testShipClassConstructor(self):
        self.assertTrue(ShipClass("LIFTER", "Lifter"))
        self.assertTrue(ShipClass("LIFTER", "Lifter", maxDeltaV=1000))

    def testShipClassAttributes(self):
        sc = ShipClass("LIFTER", "Lifter")
        self.assertTrue(hasattr(sc, "name"))
        self.assertTrue(hasattr(sc, "id"))
        self.assertTrue(hasattr(sc, "maxDeltaV"))
