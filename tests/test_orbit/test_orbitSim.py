import unittest

import json

from orbitsim.orbitSim import OrbitSim
from orbitsim.particle import Particle

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

class TestOrbitSimProperties(unittest.TestCase):
    def setUp(self):
        self.os = OrbitSim("test_json/test_orbits/happy_case.json")

    def testOrbitSimLink0(self):
        l0 = self.os.linkById(0)
        self.assertEqual(l0.deltaV, 1000)
        self.assertEqual(l0.travelTime, 10000)
        self.assertEqual(l0.distance, 100000)

    def testOrbitSimLink1(self):
        l1 = self.os.linkById(1)
        self.assertEqual(l1.deltaV, 500)
        self.assertEqual(l1.travelTime, 100000)
        self.assertEqual(l1.distance, 200000)

    def testOrbitSimLinkAll(self):
        for l in self.os._links.values():
            self.assertGreater(l.deltaV, 0)
            self.assertGreater(l.travelTime, 0)
            self.assertGreater(l.travelTime, 0)

class TestOrbitSimParticleCreation(unittest.TestCase):
    def setUp(self):
        self.os = OrbitSim("test_json/test_orbits/happy_case.json")
        self.n0 = self.os.nodeById(0)
        self.os.createParticle(self.n0)
        self.os.createParticle(self.n0)
        self.l0 = self.os.linkById(0)
        self.os.createParticle(self.l0)

    def testOrbitSimParticleCreationLength(self):
        self.assertEqual(len(self.n0.particles), 2)
        self.assertEqual(len(self.os._particles), 3)
        self.assertEqual(len(self.l0.particles), 1)

    def testOrbitSimParticleCreationTypes(self):
        for p in self.os._particles.values():
            self.assertTrue(isinstance(p, Particle))
        for p in self.n0.particles:
            self.assertFalse(isinstance(p, Particle))
        for p in self.l0.particles:
            self.assertFalse(isinstance(p, Particle))

    def testOrbitSimParticleCreationIds(self):
        for i in (0, 1):
            self.assertTrue(i in self.n0.particles)
        for i in (2,):
            self.assertTrue(i in self.l0.particles)
        for i in (0, 1, 2):
            self.assertTrue(i in self.os._particles.keys())
            self.assertEqual(self.os._particles[i].id, i)


class TestOrbitSimParticleDestruction(unittest.TestCase):
    def setUp(self):
        self.os = OrbitSim("test_json/test_orbits/happy_case.json")
        self.n0 = self.os.nodeById(0)
        self.l0 = self.os.linkById(0)
        for i in range(10):
            self.os.createParticle(self.n0)
            self.os.createParticle(self.l0)

    def testOrbitSimParticleDestructionNode(self):
        self.os.destroyParticle(2)
        self.assertEqual(len(self.os._particles), 19)
        with self.assertRaises(KeyError):
            self.os._particleLocation(2)
        self.assertFalse(2 in self.n0.particles)

        self.os.destroyParticle(3)
        self.assertEqual(len(self.os._particles), 18)
        with self.assertRaises(KeyError):
            self.os._particleLocation(2)
        self.assertFalse(3 in self.l0.particles)

        self.os.createParticle(self.n0)
        self.assertEqual(len(self.os._particles), 19)
        try:
            self.os.particleById(20)
        except KeyError:
            self.fail("particleById threw KeyError for id 20!")
        self.assertEqual(self.os.particleById(20).id, 20)


class TestOrbitSimParticleTransit(unittest.TestCase):
    def setUp(self):
        self.os = OrbitSim("test_json/test_orbits/happy_case.json")
        self.n0 = self.os.nodeById(0)
        self.l0 = self.os.linkById(0)
        for i in range(10):
            self.os.createParticle(self.n0)
            self.os.createParticle(self.l0)

    def testOrbitSimParticleTransitToLink(self):
        self.os.transitParticle(0, self.l0.id)
        self.assertTrue(0 in self.l0.particles)
        self.assertTrue(0 not in self.n0.particles)

    def testOrbitSimParticleTransitToNode(self):
        self.os.transitParticle(1, self.n0.id)
        self.assertTrue(1 in self.n0.particles)
        self.assertTrue(1 not in self.l0.particles)

    def testOrbitSimParticleTransitInvalidParticle(self):
        with self.assertRaises(KeyError):
            self.os.transitParticle(30, self.n0.id)

    def testOrbitSimParticleTransitInvalidTarget(self):
        with self.assertRaises(KeyError):
            self.os.transitParticle(1, 50)