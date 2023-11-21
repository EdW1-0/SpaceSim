import unittest

from planetsim import SurfaceBase, SurfacePoint


class ContentMock:
    pass


class TestSurfaceBase(unittest.TestCase):
    def testSurfaceBase(self):
        self.assertTrue(SurfaceBase)
        self.assertTrue(
            SurfaceBase(0, ContentMock(), SurfacePoint(0, 0), colonyId="HAD")
        )

    def testSurfaceBaseAttributes(self):
        self.assertTrue(
            hasattr(
                SurfaceBase(0, ContentMock(), SurfacePoint(0, 0), colonyId="MAR"), "id"
            )
        )
        self.assertTrue(
            hasattr(
                SurfaceBase(0, ContentMock(), SurfacePoint(0, 0), colonyId="TIT"),
                "point",
            )
        )
        self.assertTrue(
            hasattr(
                SurfaceBase(0, ContentMock(), SurfacePoint(0, 0), colonyId="VRA"),
                "content",
            )
        )
        self.assertTrue(
            hasattr(
                SurfaceBase(0, ContentMock(), SurfacePoint(0, 0), colonyId="LLP"),
                "name",
            )
        )
