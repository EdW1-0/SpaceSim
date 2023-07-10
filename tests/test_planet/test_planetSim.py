from planetsim.planetSim import PlanetSim

import unittest

class TestPlanetSim(unittest.TestCase):
    def testPlanetSimImport(self):
        self.assertTrue(PlanetSim)

    def testPlanetSimAttributes(self):
        self.assertTrue(hasattr(PlanetSim(None, "json/Planets.json"), "planets"))

    def testPlanetSimConstructor(self):
        with self.assertRaises(FileNotFoundError):
            PlanetSim(None, "")
        self.assertTrue(PlanetSim(None, jsonPath = "json/Planets.json"))
        self.assertNotEqual(len(PlanetSim(None, jsonPath = "json/Planets.json").planets), 0)

class TestPlanetSimInteraction(unittest.TestCase):

    def setUp(self):
        self.planetSim = PlanetSim(None, "json/Planets.json")
        

    def test_planetSimAccessBadNode(self):
        with self.assertRaises(KeyError):
            self.planetSim.planetById(-1)
        with self.assertRaises(ValueError):
            self.planetSim.planetById("Foo")
        with self.assertRaises(KeyError):
            self.planetSim.planetById(99)

    def test_planetSimAccessNode(self):
        self.assertNotEqual(self.planetSim.planetById("MERCURY"), None)