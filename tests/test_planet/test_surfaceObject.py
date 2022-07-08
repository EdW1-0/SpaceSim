import unittest

from planetsim.surfaceObject import SurfaceObject

class TestSurfaceObject(unittest.TestCase):
    def testSurfaceObject(self):
        self.assertTrue(SurfaceObject)
        self.assertTrue(SurfaceObject())

    def testSurfaceObjectAttributes(self):
        self.assertTrue(hasattr(SurfaceObject(), "point"))
        self.assertTrue(hasattr(SurfaceObject(), "content"))
        self.assertTrue(hasattr(SurfaceObject(), "maxV"))
        self.assertTrue(hasattr(SurfaceObject(), "fuel"))
        self.assertTrue(hasattr(SurfaceObject(), "destination"))