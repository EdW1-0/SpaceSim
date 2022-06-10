import unittest

from orbitsim.orbitLink import OrbitLink

class NodeMock:
    pass

class TestOrbitLink(unittest.TestCase):
    def testOrbitLink(self):
        self.assertTrue(OrbitLink)
        self.assertTrue(OrbitLink(0, 0, 1))

class TestOrbitLinkAttributes(unittest.TestCase):
    def testOrbitLinkAttributes(self):
        self.assertTrue(hasattr(OrbitLink(0, 0, 1), "topNode"))
        self.assertTrue(hasattr(OrbitLink(0, 0, 1), "bottomNode"))
        self.assertTrue(hasattr(OrbitLink(0, 0, 1), "particles"))
        self.assertTrue(hasattr(OrbitLink(0, 0, 1), "deltaV"))
        self.assertTrue(hasattr(OrbitLink(0, 0, 1), "travelTime"))
        self.assertTrue(hasattr(OrbitLink(0, 0, 1), "distance"))
        self.assertTrue(hasattr(OrbitLink(0, 0, 1), "id"))

class TestOrbitLinkConstructor(unittest.TestCase):
    def testOrbitLinkConstructor(self):
        with self.assertRaises(TypeError):
            OrbitLink()
        with self.assertRaises(TypeError):
            OrbitLink(0)
        with self.assertRaises(TypeError):
            OrbitLink(0, None, None)
        with self.assertRaises(TypeError):
            OrbitLink(0,0,0)

        self.assertTrue(OrbitLink(0, topNode = 0, bottomNode = 1))
        self.assertTrue(OrbitLink(id = 0, topNode = 0, bottomNode = 1, deltaV = 3.0, travelTime = 1000, distance = 10000))


class TestOrbitLinkConnections(unittest.TestCase):
    def testOrbitLinkConnections(self):
        pass

class TestOrbitLinkParticles(unittest.TestCase):
    def setUp(self):
        self.l0 = OrbitLink(0, 0, 1)

    def testOrbitNodeParticlesIsSet(self):
        with self.assertRaises(TypeError):
            self.l0.particles[0]

        self.l0.particles.add(1)
        self.l0.particles.add(1)

        self.assertEqual(len(self.l0.particles), 1)
        self.assertTrue(1 in self.l0.particles)