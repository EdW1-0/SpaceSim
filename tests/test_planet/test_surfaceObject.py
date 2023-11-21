import unittest

from planetsim import SurfaceObject, SurfacePoint


class ContentMock:
    pass


class TestSurfaceObject(unittest.TestCase):
    def testSurfaceObject(self):
        self.assertTrue(SurfaceObject)
        self.assertTrue(SurfaceObject(0, ContentMock(), SurfacePoint(0, 0)))

    def testSurfaceObjectAttributes(self):
        self.assertTrue(
            hasattr(SurfaceObject(0, ContentMock(), SurfacePoint(0, 0)), "id")
        )
        self.assertTrue(
            hasattr(SurfaceObject(0, ContentMock(), SurfacePoint(0, 0)), "point")
        )
        self.assertTrue(
            hasattr(SurfaceObject(0, ContentMock(), SurfacePoint(0, 0)), "content")
        )
        self.assertTrue(
            hasattr(SurfaceObject(0, ContentMock(), SurfacePoint(0, 0)), "name")
        )

    def testSurfaceObjectConstructor(self):
        self.assertTrue(SurfaceObject(0, ContentMock(), SurfacePoint(20, 20)))
        cm = ContentMock()
        self.assertEqual(SurfaceObject(3, cm, SurfacePoint(10, 10)).content, cm)
        self.assertEqual(SurfaceObject(3, cm, SurfacePoint(10, 10)).id, 3)

    def testSurfaceObjectKill(self):
        so = SurfaceObject(0, ContentMock(), SurfacePoint(10, 10))
        self.assertFalse(so.killed)
        so.kill()
        self.assertTrue(so.killed)
