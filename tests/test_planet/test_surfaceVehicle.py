import unittest

from planetsim.surfaceVehicle import SurfaceVehicle
from planetsim.surfacePoint import SurfacePoint

class ContentMock:
    pass

class TestSurfaceVehicle(unittest.TestCase):
    def testSurfaceVehicle(self):
        self.assertTrue(SurfaceVehicle)
        self.assertTrue(SurfaceVehicle(0, ContentMock(), SurfacePoint(0,0)))

    def testSurfaceVehicleAttributes(self):
        self.assertTrue(hasattr(SurfaceVehicle(0, ContentMock(), SurfacePoint(0,0)), "id"))
        self.assertTrue(hasattr(SurfaceVehicle(0, ContentMock(), SurfacePoint(0,0)), "point"))
        self.assertTrue(hasattr(SurfaceVehicle(0, ContentMock(), SurfacePoint(0,0)), "content"))
        self.assertTrue(hasattr(SurfaceVehicle(0, ContentMock(), SurfacePoint(0,0)), "name"))
        self.assertTrue(hasattr(SurfaceVehicle(0, ContentMock(), SurfacePoint(0,0)), "maxV"))
        self.assertTrue(hasattr(SurfaceVehicle(0, ContentMock(), SurfacePoint(0,0)), "fuel"))
        self.assertTrue(hasattr(SurfaceVehicle(0, ContentMock(), SurfacePoint(0,0)), "destination"))
        self.assertTrue(hasattr(SurfaceVehicle(0, ContentMock(), SurfacePoint(0,0)), "fuelPerM"))

    def testSurfaceVehicleConstructor(self):
        self.assertTrue(SurfaceVehicle(0, ContentMock(), SurfacePoint(20, 20)))
        cm = ContentMock()
        self.assertEqual(SurfaceVehicle(3, cm, SurfacePoint(10,10)).content, cm)
        self.assertEqual(SurfaceVehicle(3, cm, SurfacePoint(10,10)).id, 3)
        self.assertEqual(SurfaceVehicle(3, cm, SurfacePoint(10,10)).point, SurfacePoint(10, 10))
        self.assertEqual(SurfaceVehicle(3, cm, SurfacePoint(10,10), fuel = 100).fuel, 100)
        self.assertEqual(SurfaceVehicle(3, cm, SurfacePoint(10,10), maxV = 10).maxV, 10)
        self.assertEqual(SurfaceVehicle(3, cm, SurfacePoint(10,10), fuelPerM = 5.3).fuelPerM, 5.3)
        

    def testSurfaceVehicleSetTarget(self):
        so = SurfaceVehicle(0, ContentMock(), SurfacePoint(10,10))
        so.setDestination(SurfacePoint(50,50))
        self.assertEqual(so.destination, SurfacePoint(50, 50))