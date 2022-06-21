import unittest

from planetsim.surfaceRegion import SurfaceRegion

class TestSurfaceRegion(unittest.TestCase):
    def testSurfaceRegion(self):
        self.assertTrue(SurfaceRegion)
        self.assertTrue(SurfaceRegion())

    def testSurfaceAttributes(self):
        self.assertTrue(hasattr(SurfaceRegion(), "borders"))
        self.assertTrue(hasattr(SurfaceRegion(), "homePoint"))