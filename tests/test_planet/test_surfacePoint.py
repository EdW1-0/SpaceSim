import unittest

from math import sqrt

from planetsim.surfacePoint import (
    SurfacePoint,
    canonicalPoint,
    dot,
    cross,
    magnitude,
    pointFromVector,
    normalise,
    almostEqual,
    vector,
)


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
        self.assertEqual(SurfacePoint(0.0, 0.0).vector(), (1.0, 0.0, 0.0))

    def testSurfacePointCanonical(self):
        self.assertEqual(canonicalPoint(SurfacePoint(0.0, 0.0)), SurfacePoint(0.0, 0.0))
        self.assertEqual(
            canonicalPoint(SurfacePoint(0.0, 120.0)), SurfacePoint(0.0, 120.0)
        )
        self.assertEqual(
            canonicalPoint(SurfacePoint(0.0, 400.0)), SurfacePoint(0.0, 40.0)
        )
        self.assertEqual(
            canonicalPoint(SurfacePoint(0.0, -180.0)), SurfacePoint(0.0, 180.0)
        )
        self.assertEqual(
            canonicalPoint(SurfacePoint(110.0, 20.0)), SurfacePoint(70.0, 200.0)
        )
        self.assertEqual(
            canonicalPoint(SurfacePoint(210.0, 20.0)), SurfacePoint(-30.0, 200.0)
        )
        self.assertEqual(
            canonicalPoint(SurfacePoint(300.0, 20.0)), SurfacePoint(-60.0, 20.0)
        )
        self.assertEqual(
            canonicalPoint(SurfacePoint(400.0, 20.0)), SurfacePoint(40.0, 20.0)
        )
        self.assertEqual(
            canonicalPoint(SurfacePoint(540.0, 20.0)), SurfacePoint(0, 200.0)
        )
        self.assertEqual(
            canonicalPoint(SurfacePoint(-60.0, 20.0)), SurfacePoint(-60.0, 20.0)
        )
        self.assertEqual(
            canonicalPoint(SurfacePoint(-120.0, 20.0)), SurfacePoint(-60.0, 200.0)
        )
        self.assertEqual(
            canonicalPoint(SurfacePoint(-280.0, 20.0)), SurfacePoint(80.0, 20.0)
        )
        self.assertEqual(
            canonicalPoint(SurfacePoint(-400.0, 20.0)), SurfacePoint(-40.0, 20.0)
        )


class TestLatLong(unittest.TestCase):
    def testKnownOutput(self):
        self.assertEqual(pointFromVector((0, 0, 1)), SurfacePoint(90, 0))

    def testSelfInverse(self):
        self.assertEqual(
            pointFromVector(SurfacePoint(0, 0).vector()), SurfacePoint(0, 0)
        )
        self.assertEqual(
            pointFromVector(SurfacePoint(90, 0).vector()), SurfacePoint(90, 0)
        )
        self.assertEqual(
            pointFromVector(SurfacePoint(54, 0.1).vector()), SurfacePoint(54, 0.1)
        )
        self.assertEqual(
            pointFromVector(SurfacePoint(45, -70).vector()), SurfacePoint(45, 290)
        )


class TestVectorProducts(unittest.TestCase):
    def setUp(self):
        self.v1 = SurfacePoint(0.0, 0.0)
        self.v2 = SurfacePoint(0.0, 0.0)
        self.v3 = SurfacePoint(0.0, 90.0)
        self.v4 = SurfacePoint(90.0, 0.0)

    def testVector(self):
        self.assertAlmostEqual(vector(90.0, 0.0)[0], 0)
        self.assertAlmostEqual(vector(90.0, 0.0)[1], 0)
        self.assertAlmostEqual(vector(90.0, 0.0)[2], 1)
        self.assertEqual(vector(0.0, 0.0), (1, 0, 0))

    def testDotProduct(self):
        self.assertEqual(dot(self.v1.vector(), self.v2.vector()), 1.0)
        self.assertAlmostEqual(
            dot(self.v1.vector(), SurfacePoint(90.0, 0.0).vector()), 0.0
        )

    def testCrossProduct(self):
        self.assertEqual(cross(self.v1.vector(), self.v2.vector()), (0, 0, 0))
        self.assertEqual(
            cross(self.v1.vector(), SurfacePoint(0.0, 90.0).vector()), (0.0, 0.0, 1.0)
        )

    def testMagnitude(self):
        self.assertEqual(magnitude((1, 0, 0)), 1)

    def testNormalise(self):
        self.assertEqual(normalise((3, 0, 0)), (1, 0, 0))
        self.assertEqual(normalise((-3, 0, -4)), (-0.6, 0, -0.8))
        self.assertEqual(
            normalise((1, -1, -1)), (1 / sqrt(3), -1 / sqrt(3), -1 / sqrt(3))
        )

    def testAlmostEqual(self):
        self.assertTrue(almostEqual(SurfacePoint(0, 0), SurfacePoint(0.001, -0.001)))
