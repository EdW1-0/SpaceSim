import unittest

import json

from orbitsim.orbitSim import OrbitSim

class TestOrbitSim(unittest.TestCase):
    def testOrbitSim(self):
        self.assertNotEqual(OrbitSim, False)
        self.assertTrue(OrbitSim())

    def testOrbitSimParticles(self):
        self.assertTrue(hasattr(OrbitSim(), "_particles"))
        self.assertTrue(hasattr(OrbitSim(), "_nodes"))
        self.assertTrue(hasattr(OrbitSim(), "_links"))

    def testOrbitSimLoad(self):
        self.assertTrue(OrbitSim("test_json/test_orbits/happy_case.json"))
        with self.assertRaises(FileNotFoundError):
            OrbitSim("test_json/test_orbits/nonexistant.json")
        with self.assertRaises(json.JSONDecodeError):
            OrbitSim("test_json/test_orbits/malformed.json")
        self.assertNotEqual(OrbitSim("test_json/test_orbits/happy_case.json")._nodes, [])
