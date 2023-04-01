from views.orbitContext import OrbitContext, OrbitNodeView
from views.guiContext import GUIContext

import unittest
from tests.test_views.test_guiContext import ScreenMock, ModelMock

class OrbitNodeMock:
    pass

class TestOrbitNodeView(unittest.TestCase):
    def testOrbitNodeView(self):
        self.assertTrue(OrbitNodeView)

    def testOrbitNodeViewConstructor(self):
        onm = OrbitNodeMock()
        onm.leaf = 0
        self.assertTrue(OrbitNodeView(onm))
        self.assertTrue(hasattr(OrbitNodeView(onm), "node"))
        self.assertTrue(hasattr(OrbitNodeView(onm), "center"))
        self.assertTrue(hasattr(OrbitNodeView(onm), "surf"))
        self.assertTrue(hasattr(OrbitNodeView(onm), "rect"))

    def testOrbitNodeViewCenter(self):
        onm = OrbitNodeMock()
        onm.leaf = 0
        self.assertEqual(OrbitNodeView(onm).center, (0,0))


class TestOrbitContext(unittest.TestCase):
    def testOrbitContext(self):
        self.assertTrue(OrbitContext)

    