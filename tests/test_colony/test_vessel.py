import unittest

from colonysim.vessel import Vessel

class TestVessel(unittest.TestCase):
    def setUp(self):
        self.v = Vessel()

    def testAddCargo(self):
        self.v.addCargo({"H2O": 500, "BAUXITE": 100})
        self.assertEqual(self.v.cargo["BAUXITE"], 100)
        self.assertEqual(self.v.cargo["H2O"], 500)
        self.v.addCargo({"H2O": 10000})
        self.assertEqual(self.v.cargo["H2O"], 10500)

    def testRemoveCargo(self):
        self.v.addCargo({"NH3": 5000, "CH4": 2000})
        retDict = self.v.removeCargo({"NH3":500, "CH4": 3000, "H2": 200})
        self.assertEqual(retDict["NH3"], 500)
        self.assertEqual(retDict["CH4"], 2000)
        self.assertEqual(retDict["H2"], 0)
        with self.assertRaises(KeyError):
            self.v.cargo["CH4"]
        self.assertEqual(self.v.cargo["NH3"], 4500)