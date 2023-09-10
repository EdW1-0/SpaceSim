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

class TestShipCargo(unittest.TestCase):
    def setUp(self):
        self.sc = ShipClass("TEST", "Test", 100)
        self.s = Ship(0, "Ship 1", self.sc)

    def testAddCargo(self):
        self.s.addCargo({"H2O": 500, "BAUXITE": 100})
        self.assertEqual(self.s.cargo["BAUXITE"], 100)
        self.assertEqual(self.s.cargo["H2O"], 500)
        self.s.addCargo({"H2O": 10000})
        self.assertEqual(self.s.cargo["H2O"], 10500)

    def testRemoveCargo(self):
        self.s.addCargo({"NH3": 5000, "CH4": 2000})
        retDict = self.s.removeCargo({"NH3":500, "CH4": 3000, "H2": 200})
        self.assertEqual(retDict["NH3"], 500)
        self.assertEqual(retDict["CH4"], 2000)
        self.assertEqual(retDict["H2"], 0)
        with self.assertRaises(KeyError):
            self.s.cargo["CH4"]
        self.assertEqual(self.s.cargo["NH3"], 4500)

    def testAddNegativeCargo(self):
        self.skipTest()

    def testRemoveNegativeCargo(self):
        self.skipTest()