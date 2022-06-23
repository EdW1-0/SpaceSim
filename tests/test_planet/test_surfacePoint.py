import unittest

from planetsim.surfacePoint import SurfacePoint, normalisePoint

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

    def testSurfacePointVectorRep(self):
        self.assertEqual(SurfacePoint(0.0,0.0).vector(), (1.0, 0.0, 0.0))

    def testSurfacePointNormalise(self):
        self.assertEqual(normalisePoint(SurfacePoint(0.0,0.0)), SurfacePoint(0.0,0.0))
        self.assertEqual(normalisePoint(SurfacePoint(0.0,120.0)), SurfacePoint(0.0,120.0))
        self.assertEqual(normalisePoint(SurfacePoint(0.0,400.0)), SurfacePoint(0.0,40.0))
        self.assertEqual(normalisePoint(SurfacePoint(0.0,-180.0)), SurfacePoint(0.0,180.0))
        self.assertEqual(normalisePoint(SurfacePoint(110.0,20.0)), SurfacePoint(70.0,200.0))
        self.assertEqual(normalisePoint(SurfacePoint(210.0,20.0)), SurfacePoint(-30.0,200.0))
        self.assertEqual(normalisePoint(SurfacePoint(300.0,20.0)), SurfacePoint(-60.0,20.0))
        self.assertEqual(normalisePoint(SurfacePoint(400.0,20.0)), SurfacePoint(40.0, 20.0))
        self.assertEqual(normalisePoint(SurfacePoint(540.0,20.0)), SurfacePoint(0, 200.0))
        self.assertEqual(normalisePoint(SurfacePoint(-60.0, 20.0)), SurfacePoint(-60.0, 20.0))
        self.assertEqual(normalisePoint(SurfacePoint(-120.0, 20.0)), SurfacePoint(-60.0, 200.0))
        self.assertEqual(normalisePoint(SurfacePoint(-280.0, 20.0)), SurfacePoint(80.0, 20.0))
        self.assertEqual(normalisePoint(SurfacePoint(-400.0, 20.0)), SurfacePoint(-40.0, 20.0))
        
        
        
        
        
        