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
        self.assertNotEqual(OrbitSim("test_json/test_orbits/happy_case.json")._nodes, {})
        self.assertEqual(len(OrbitSim("test_json/test_orbits/happy_case.json")._nodes), 4)
        self.assertEqual(len(OrbitSim("test_json/test_orbits/happy_case.json")._links), 3)
        
class TestOrbitSimNodes(unittest.TestCase):
    def setUp(self):
        self.os = OrbitSim("test_json/test_orbits/happy_case.json")

    def testOrbitSimNodeById(self):
        self.assertTrue(self.os.nodeById(0))
        with self.assertRaises(TypeError):
            OrbitSim().nodeById("Sun")
        with self.assertRaises(ValueError):
            OrbitSim().nodeById(-1)
    
    def testOrbitSimNode0(self):
        n0 = self.os.nodeById(0)
        self.assertEqual(n0.id, 0)
        self.assertEqual(n0.name, "Sun")
        self.assertEqual(n0.gravity, 100)

    def testOrbitSimNode1(self):
        n1 = self.os.nodeById(1)
        self.assertEqual(n1.id, 1)
        self.assertEqual(n1.name, "Sun Low Orbit")
        self.assertEqual(n1.gravity, 0)

class TestOrbitSimLinks(unittest.TestCase):
    def setUp(self):
        self.os = OrbitSim("test_json/test_orbits/happy_case.json")

    def testOrbitSimLinkById(self):
        self.assertTrue(self.os.linkById(0))
        with self.assertRaises(TypeError):
            OrbitSim().linkById("Sun")
        with self.assertRaises(ValueError):
            OrbitSim().linkById(-1)

    def testOrbitSimLinkage(self):
        self.assertEqual(self.os.linkById(0).topNode, 1)
        self.assertEqual(self.os.linkById(0).bottomNode, 0)
        self.assertEqual(self.os.nodeById(0).links, [0, 1])
        self.assertEqual(self.os.nodeById(1).links, [0, 2])

    def testOrbitSimLinkageMultidrop(self):
        self.assertTrue(self.os.linkById(1))
        self.assertEqual(self.os.linkById(1).topNode, 3)
        self.assertEqual(self.os.linkById(1).bottomNode, 0)
        self.assertEqual(self.os.nodeById(3).links, [1])
        
    def testOrbitSimMultiLink(self):
        self.assertTrue(self.os.linkById(2))
        self.assertEqual(self.os.linkById(2).topNode, 2)
        self.assertEqual(self.os.linkById(2).bottomNode, 1)
        self.assertEqual(self.os.nodeById(1).links, [0, 2])
        self.assertEqual(self.os.nodeById(2).links, [2])




