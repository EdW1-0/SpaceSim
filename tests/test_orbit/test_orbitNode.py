import unittest

from orbitsim.orbitNode import OrbitNode

class PlanetMock:
    pass

class TestOrbitNode(unittest.TestCase):
    def testOrbitNode(self):
        self.assertTrue(OrbitNode)
        self.assertTrue(OrbitNode(0))

class TestOrbitNodeAttributes(unittest.TestCase):
    def testOrbitNodeAttributes(self):
        self.assertTrue(hasattr(OrbitNode(0), "particles"))
        self.assertTrue(hasattr(OrbitNode(0), "links"))
        self.assertTrue(hasattr(OrbitNode(0), "planet"))
        self.assertTrue(hasattr(OrbitNode(0), "gravity"))
        self.assertTrue(hasattr(OrbitNode(0), "name"))
        self.assertTrue(hasattr(OrbitNode(0), "id"))

class TestOrbitNodeConstructor(unittest.TestCase):
    def testOrbitNodeConstructor(self):
        with self.assertRaises(TypeError):
            OrbitNode()
        self.assertTrue(OrbitNode(0))
        self.assertTrue(OrbitNode(0, planet = PlanetMock()))
        self.assertTrue(OrbitNode(id = 0, planet = PlanetMock(), gravity = 9.8))

class TestOrbitNodeLinks(unittest.TestCase):
    def testOrbitNodeLinks(self):
        self.assertEqual(OrbitNode(0).links, [])

class TestOrbitNodeParticles(unittest.TestCase):
    def setUp(self):
        self.n0 = OrbitNode(0)

    def testOrbitNodeParticlesIsSet(self):
        with self.assertRaises(TypeError):
            self.n0.particles[0]

        self.n0.particles.add(1)
        self.n0.particles.add(1)

        self.assertEqual(len(self.n0.particles), 1)
        self.assertTrue(1 in self.n0.particles)

        