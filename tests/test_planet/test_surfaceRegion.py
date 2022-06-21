import unittest

from planetsim.surfaceRegion import SurfaceRegion

class TestSurfaceRegion(unittest.TestCase):
    def testSurfaceRegion(self):
        self.assertTrue(SurfaceRegion)
        self.assertTrue(SurfaceRegion(0, [], []))

    def testSurfaceAttributes(self):
        self.assertTrue(hasattr(SurfaceRegion(0, [], []), "id"))
        self.assertTrue(hasattr(SurfaceRegion(0, [], []), "borders"))
        self.assertTrue(hasattr(SurfaceRegion(0, [], []), "homePoint"))