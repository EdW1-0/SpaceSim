import unittest

from planetsim.surfacePoint import SurfacePoint

class TestSurfacePoint(unittest.TestCase):
    def testSurfacePoint(self):
        self.assertTrue(SurfacePoint)
        self.assertTrue(SurfacePoint(0.0, 0.0))

    def testSurfacePointAttributes(self):
        self.assertTrue(hasattr(SurfacePoint(0.0, 0.0), "latitude"))
        self.assertTrue(hasattr(SurfacePoint(0, 0), "longitude"))

    def testSurfacePointConstructor(self):
        self.assertTrue(SurfacePoint(40.0, 75.0))
        self.assertEqual(SurfacePoint(-40.0, 70.0).latitude, -40.0)
        self.assertEqual(SurfacePoint(-40.0, 60.0).longitude, 60.0)