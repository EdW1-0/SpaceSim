import unittest

from views.orbitContext import OrbitNodeView

from orbitsim.orbitNode import OrbitNode, LeafClass

class TestOrbitNodeView(unittest.TestCase):
    def setUp(self):
        self.on = OrbitNode(0, "Sun")
        

    def testOrbitNodeView(self):
        self.assertTrue(OrbitNodeView)

    def testOrbitNodeViewConstructor(self):
        self.assertTrue(OrbitNodeView(self.on))
        self.assertTrue(OrbitNodeView(self.on, center = (1,1)))
        self.assertTrue(OrbitNodeView(self.on, center = (1,1), selected = True))

    def testOrbitNodeViewAttributes(self):
        onv = OrbitNodeView(self.on)
        self.assertTrue(hasattr(onv, "rect"))
        self.assertTrue(hasattr(onv, "surf"))
        self.assertTrue(hasattr(onv, "center"))
        self.assertTrue(hasattr(onv, "node"))
