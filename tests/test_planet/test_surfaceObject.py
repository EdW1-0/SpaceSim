import unittest

from planetsim.surfaceObject import SurfaceObject
from planetsim.surfacePoint import SurfacePoint

class ContentMock:
    pass

class TestSurfaceObject(unittest.TestCase):
    def testSurfaceObject(self):
        self.assertTrue(SurfaceObject)
        self.assertTrue(SurfaceObject(0, ContentMock(), SurfacePoint(0,0)))

    def testSurfaceObjectAttributes(self):
        self.assertTrue(hasattr(SurfaceObject(0, ContentMock(), SurfacePoint(0,0)), "id"))
        self.assertTrue(hasattr(SurfaceObject(0, ContentMock(), SurfacePoint(0,0)), "point"))
        self.assertTrue(hasattr(SurfaceObject(0, ContentMock(), SurfacePoint(0,0)), "content"))
        self.assertTrue(hasattr(SurfaceObject(0, ContentMock(), SurfacePoint(0,0)), "maxV"))
        self.assertTrue(hasattr(SurfaceObject(0, ContentMock(), SurfacePoint(0,0)), "fuel"))
        self.assertTrue(hasattr(SurfaceObject(0, ContentMock(), SurfacePoint(0,0)), "destination"))
        self.assertTrue(hasattr(SurfaceObject(0, ContentMock(), SurfacePoint(0,0)), "fuelPerM"))

    def testSurfaceObjectConstructor(self):
        self.assertTrue(SurfaceObject(0, ContentMock(), SurfacePoint(20, 20)))
        cm = ContentMock()
        self.assertEqual(SurfaceObject(3, cm, SurfacePoint(10,10)).content, cm)
        self.assertEqual(SurfaceObject(3, cm, SurfacePoint(10,10)).id, 3)
        self.assertEqual(SurfaceObject(3, cm, SurfacePoint(10,10)).point, SurfacePoint(10, 10))
        self.assertEqual(SurfaceObject(3, cm, SurfacePoint(10,10), fuel = 100).fuel, 100)
        self.assertEqual(SurfaceObject(3, cm, SurfacePoint(10,10), maxV = 10).maxV, 10)
        self.assertEqual(SurfaceObject(3, cm, SurfacePoint(10,10), fuelPerM = 5.3).fuelPerM, 5.3)
        

    def testSurfaceObjectSetTarget(self):
        so = SurfaceObject(0, ContentMock(), SurfacePoint(10,10))
        so.setDestination(SurfacePoint(50,50))
        self.assertEqual(so.destination, SurfacePoint(50, 50))
        