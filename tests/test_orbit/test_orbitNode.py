import unittest

from orbitsim.orbitNode import OrbitNode

class PlanetMock:
    pass

class TestOrbitNode(unittest.TestCase):
    def testOrbitNode(self):
        self.assertTrue(OrbitNode)
        self.assertTrue(OrbitNode())

class TestOrbitNodeAttributes(unittest.TestCase):
    def testOrbitNodeAttributes(self):
        self.assertTrue(hasattr(OrbitNode(), "particles"))
        self.assertTrue(hasattr(OrbitNode(), "links"))
        self.assertTrue(hasattr(OrbitNode(), "planet"))
        self.assertTrue(hasattr(OrbitNode(), "gravity"))

class TestOrbitNodeConstructor(unittest.TestCase):
    def testOrbitNodeConstructor(self):
        self.assertTrue(OrbitNode())
        self.assertTrue(OrbitNode(planet = PlanetMock()))
        self.assertTrue(OrbitNode(planet = PlanetMock(), gravity = 9.8))

class TestOrbitNodeLinks(unittest.TestCase):
    def testOrbitNodeLinks(self):
        self.assertEqual(OrbitNode().links, [])
