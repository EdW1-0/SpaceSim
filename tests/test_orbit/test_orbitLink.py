import unittest

from orbitsim.orbitLink import OrbitLink

class NodeMock:
    pass

class TestOrbitLink(unittest.TestCase):
    def testOrbitLink(self):
        self.assertTrue(OrbitLink)
        self.assertTrue(OrbitLink(NodeMock(), NodeMock()))

class TestOrbitLinkAttributes(unittest.TestCase):
    def testOrbitLinkAttributes(self):
        self.assertTrue(hasattr(OrbitLink(NodeMock(), NodeMock()), "topNode"))
        self.assertTrue(hasattr(OrbitLink(NodeMock(), NodeMock()), "bottomNode"))
        self.assertTrue(hasattr(OrbitLink(NodeMock(), NodeMock()), "particles"))
        self.assertTrue(hasattr(OrbitLink(NodeMock(), NodeMock()), "deltaV"))
        self.assertTrue(hasattr(OrbitLink(NodeMock(), NodeMock()), "travelTime"))
        self.assertTrue(hasattr(OrbitLink(NodeMock(), NodeMock()), "distance"))

class TestOrbitLinkConstructor(unittest.TestCase):
    def testOrbitLinkConstructor(self):
        with self.assertRaises(TypeError):
            OrbitLink()
        with self.assertRaises(TypeError):
            OrbitLink(None, None)

        self.assertTrue(OrbitLink(topNode = NodeMock(), bottomNode = NodeMock()))
        self.assertTrue(OrbitLink(topNode = NodeMock(), bottomNode = NodeMock(), deltaV = 3.0, travelTime = 1000, distance = 10000))


class TestOrbitLinkConnections(unittest.TestCase):
    def testOrbitLinkConnections(self):
        pass
