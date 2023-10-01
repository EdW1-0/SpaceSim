import unittest

import math

from planetsim.surfacePath import SurfacePath, gcIntersections, pathsIntersect
from planetsim.surfacePoint import (
    SurfacePoint,
    canonicalPoint,
    pointFromVector,
    almostEqual,
)


class TestSurfacePath(unittest.TestCase):
    def testSurfacePathInit(self):
        self.assertTrue(SurfacePath)
        self.assertTrue(SurfacePath(SurfacePoint(0, 0), SurfacePoint(0, 0)))

    def testSurfacePathAttributes(self):
        self.assertTrue(hasattr(SurfacePath(), "p1"))
        self.assertTrue(hasattr(SurfacePath(), "p2"))
        self.assertTrue(hasattr(SurfacePath(), "long"))

    def testSurfacePathConstructor(self):
        self.assertEqual(SurfacePath(p1=SurfacePoint(30, 60)).p1, SurfacePoint(30, 60))
        self.assertEqual(
            SurfacePath(p2=SurfacePoint(-40, 270)).p2, SurfacePoint(-40, 270)
        )
        self.assertEqual(SurfacePath().long, False)
        self.assertEqual(SurfacePath(long=True).long, True)


class TestSurfacePathGeodetics(unittest.TestCase):
    def testGreatCircleAngle(self):
        self.assertEqual(
            SurfacePath(SurfacePoint(0.0, 0.0), SurfacePoint(0.0, 0.0)).gcAngle(), 0.0
        )
        self.assertEqual(
            SurfacePath(SurfacePoint(0.0, 0.0), SurfacePoint(90.0, 0.0)).gcAngle(),
            math.pi / 2,
        )
        self.assertEqual(
            SurfacePath(SurfacePoint(0.0, 0.0), SurfacePoint(0.0, 180.0)).gcAngle(),
            math.pi,
        )

    def testGreatCircleDegeneratePath(self):
        meridianGc = SurfacePath(SurfacePoint(90, 45), SurfacePoint(0, 45)).gc()
        degGc = SurfacePath(SurfacePoint(10, 45), SurfacePoint(10, 45)).gc()
        for i in range(3):
            self.assertAlmostEqual(meridianGc[i], degGc[i])

    def testGreatCircleDegeneratePathOffDiagonal(self):
        meridianGc = SurfacePath(SurfacePoint(90, 10), SurfacePoint(0, 10)).gc()
        degGc = SurfacePath(SurfacePoint(0, 10), SurfacePoint(0, 10)).gc()
        for i in range(3):
            self.assertAlmostEqual(meridianGc[i], degGc[i])

    def testGreatCircleDegeneratePathOnPrime(self):
        meridianGc = SurfacePath(SurfacePoint(90, 0), SurfacePoint(0, 0)).gc()
        degGc = SurfacePath(SurfacePoint(0, 0), SurfacePoint(0, 0)).gc()
        for i in range(3):
            self.assertAlmostEqual(meridianGc[i], degGc[i])

    def testGreatCircleDegeneratePathHighLongitude(self):
        meridianGc = SurfacePath(SurfacePoint(-90, 220), SurfacePoint(0, 220)).gc()
        degGc = SurfacePath(SurfacePoint(0, 220), SurfacePoint(0, 220)).gc()
        for i in range(3):
            # We end up flipped 180, but because it's a great circle
            # this is actually the same path.
            # We don't care about the direction.
            self.assertAlmostEqual(meridianGc[i], -degGc[i])

    def testGreatCircleDegeneratePathPolar(self):
        meridianGc = SurfacePath(SurfacePoint(90, 0), SurfacePoint(0, 0)).gc()
        degGc = SurfacePath(SurfacePoint(90, 0), SurfacePoint(90, 0)).gc()
        for i in range(3):
            self.assertAlmostEqual(meridianGc[i], degGc[i])

    def testPathIsMeridian(self):
        self.assertTrue(
            SurfacePath(SurfacePoint(0.0, 0.0), SurfacePoint(80.0, 0.0)).isMeridian()
        )
        self.assertFalse(
            SurfacePath(SurfacePoint(0.0, 0.0), SurfacePoint(80.0, 10.0)).isMeridian()
        )
        self.assertTrue(
            SurfacePath(SurfacePoint(70.0, 0.0), SurfacePoint(70.0, 180.0)).isMeridian()
        )
        self.assertTrue(
            SurfacePath(
                SurfacePoint(-70.0, 0.0), SurfacePoint(-60.0, 180.0)
            ).isMeridian()
        )

    def testPathCrossesDateline(self):
        self.assertTrue(
            SurfacePath(
                SurfacePoint(0.0, 340.0), SurfacePoint(80.0, 20.0)
            ).crossesDateline()
        )
        self.assertFalse(
            SurfacePath(
                SurfacePoint(0.0, 40.0), SurfacePoint(80.0, 60.0)
            ).crossesDateline()
        )
        self.assertFalse(
            SurfacePath(
                SurfacePoint(0.0, 340.0), SurfacePoint(80.0, 60.0), long=True
            ).crossesDateline()
        )
        self.assertTrue(
            SurfacePath(
                SurfacePoint(0.0, 90.0), SurfacePoint(10.0, 110.0), long=True
            ).crossesDateline()
        )

    def testPathIsNorthPolar(self):
        self.assertTrue(
            SurfacePath(
                SurfacePoint(80.0, 50.0), SurfacePoint(80.0, 230.0)
            ).isNorthPolar()
        )
        self.assertTrue(
            SurfacePath(
                SurfacePoint(0.0, 50.0), SurfacePoint(0.0, 230.0)
            ).isNorthPolar()
        )
        self.assertTrue(
            SurfacePath(
                SurfacePoint(70.0, 50.0), SurfacePoint(-60.0, 230.0)
            ).isNorthPolar()
        )
        self.assertTrue(
            SurfacePath(
                SurfacePoint(-10.0, 50.0), SurfacePoint(-10.0, 230.0), long=True
            ).isNorthPolar()
        )
        self.assertFalse(
            SurfacePath(
                SurfacePoint(80.0, 50.0), SurfacePoint(80.0, 230.0), long=True
            ).isNorthPolar()
        )
        self.assertFalse(
            SurfacePath(
                SurfacePoint(-10.0, 50.0), SurfacePoint(-10.0, 230.0)
            ).isNorthPolar()
        )
        self.assertFalse(
            SurfacePath(
                SurfacePoint(70.0, 50.0), SurfacePoint(80.0, 50.0)
            ).isNorthPolar()
        )
        self.assertFalse(
            SurfacePath(
                SurfacePoint(80.0, 50.0), SurfacePoint(80.0, 240.0)
            ).isNorthPolar()
        )

    def testPathIsSouthPolar(self):
        self.assertFalse(
            SurfacePath(
                SurfacePoint(80.0, 50.0), SurfacePoint(80.0, 230.0)
            ).isSouthPolar()
        )
        self.assertFalse(
            SurfacePath(
                SurfacePoint(0.0, 50.0), SurfacePoint(0.0, 230.0)
            ).isSouthPolar()
        )
        self.assertFalse(
            SurfacePath(
                SurfacePoint(70.0, 50.0), SurfacePoint(-60.0, 230.0)
            ).isSouthPolar()
        )
        self.assertFalse(
            SurfacePath(
                SurfacePoint(-10.0, 50.0), SurfacePoint(-10.0, 230.0), long=True
            ).isSouthPolar()
        )
        self.assertTrue(
            SurfacePath(
                SurfacePoint(80.0, 50.0), SurfacePoint(80.0, 230.0), long=True
            ).isSouthPolar()
        )
        self.assertTrue(
            SurfacePath(
                SurfacePoint(-10.0, 50.0), SurfacePoint(-10.0, 230.0)
            ).isSouthPolar()
        )
        self.assertFalse(
            SurfacePath(
                SurfacePoint(70.0, 50.0), SurfacePoint(80.0, 50.0)
            ).isSouthPolar()
        )
        self.assertFalse(
            SurfacePath(
                SurfacePoint(80.0, 50.0), SurfacePoint(80.0, 240.0)
            ).isSouthPolar()
        )

    def testPathIsDoublePolar(self):
        self.assertTrue(
            SurfacePath(
                SurfacePoint(-60.0, 100.0), SurfacePoint(80.0, 100.0), long=True
            ).isDoublePolar()
        )
        self.assertFalse(
            SurfacePath(
                SurfacePoint(-60.0, 100.0), SurfacePoint(80.0, 100.0)
            ).isDoublePolar()
        )
        self.assertFalse(
            SurfacePath(
                SurfacePoint(-60.0, 110.0), SurfacePoint(80.0, 100.0), long=True
            ).isDoublePolar()
        )


class TestPointOnPath(unittest.TestCase):
    def setUp(self):
        self.path = SurfacePath(SurfacePoint(-20, 20), SurfacePoint(40, 80))
        self.datelinePath = SurfacePath(SurfacePoint(-20, 340), SurfacePoint(20, 20))
        self.meridianPath = SurfacePath(SurfacePoint(-20, 40), SurfacePoint(20, 40))
        self.polarPath = SurfacePath(SurfacePoint(70, 30), SurfacePoint(70, 210))
        self.southPolarPath = SurfacePath(SurfacePoint(-70, 30), SurfacePoint(-70, 210))
        self.polarWrappingPath = SurfacePath(
            SurfacePoint(40, 30), SurfacePoint(-40, 30), long=True
        )

    def testPointOnPath(self):
        self.assertTrue(self.path.pointOnPath(SurfacePoint(0, 50)))
        self.assertTrue(self.datelinePath.pointOnPath(SurfacePoint(0, 0)))

    def testPointNotOnPath(self):
        self.assertFalse(self.path.pointOnPath(SurfacePoint(0, 0)))
        self.assertFalse(self.path.pointOnPath(SurfacePoint(-20, 110)))


class TestPathIntersections(unittest.TestCase):
    def testPathsIntersectionPoints(self):
        path1 = SurfacePath(SurfacePoint(0, 0), SurfacePoint(0, 90))
        path2 = SurfacePath(SurfacePoint(0, 0), SurfacePoint(90, 0))
        self.assertEqual(gcIntersections(path1, path2), ((1, 0, 0), (-1, 0, 0)))
        path1 = SurfacePath(SurfacePoint(50, 20), SurfacePoint(-50, 80))
        path2 = SurfacePath(SurfacePoint(-50, 20), SurfacePoint(50, 80))
        ints = tuple(
            canonicalPoint(pointFromVector(i)) for i in gcIntersections(path1, path2)
        )
        self.assertAlmostEqual(ints[0].latitude, 0.0)
        self.assertAlmostEqual(ints[0].longitude, 50.0)
        self.assertAlmostEqual(ints[1].latitude, 0.0)
        self.assertAlmostEqual(ints[1].longitude, 230.0)

    def testPathsIntersectNoWrapNoSingularity(self):
        path1 = SurfacePath(SurfacePoint(50, 20), SurfacePoint(-50, 80))
        path2 = SurfacePath(SurfacePoint(-50, 20), SurfacePoint(50, 80))
        self.assertTrue(pathsIntersect(path1, path2))
        self.assertTrue(pathsIntersect(path2, path1))
        path3 = SurfacePath(SurfacePoint(-50, 80), SurfacePoint(50, 20))
        path4 = SurfacePath(SurfacePoint(50, 80), SurfacePoint(-50, 20))
        self.assertTrue(pathsIntersect(path3, path4))
        self.assertTrue(pathsIntersect(path4, path3))
        # Positive case

    def testPathsDontIntersectRespectsDirectionality(self):
        path1 = SurfacePath(SurfacePoint(-50, 80), SurfacePoint(50, 20), long=True)
        path2 = SurfacePath(SurfacePoint(-50, 20), SurfacePoint(50, 80))
        self.assertFalse(pathsIntersect(path1, path2))

    def testPathsDontIntersectNoWrapNoSingularity(self):
        path1 = SurfacePath(SurfacePoint(50, 20), SurfacePoint(-50, 80))
        path2 = SurfacePath(SurfacePoint(-50, 20), SurfacePoint(50, 10))
        self.assertFalse(pathsIntersect(path1, path2))

    def testPathsDontIntersectAntipodeOnOneArc(self):
        path1 = SurfacePath(SurfacePoint(50, 20), SurfacePoint(-50, 80))
        path2 = SurfacePath(SurfacePoint(-50, 20), SurfacePoint(-30, 30))
        self.assertFalse(pathsIntersect(path1, path2))

    def testPathsIntersectOnMeridian(self):
        path1 = SurfacePath(SurfacePoint(0, 20), SurfacePoint(0, 60))
        path2 = SurfacePath(SurfacePoint(-40, 40), SurfacePoint(40, 40))
        self.assertTrue(pathsIntersect(path1, path2))

    def testPathsIntersectOnDateline(self):
        path1 = SurfacePath(SurfacePoint(40, 300), SurfacePoint(-40, 60))
        path2 = SurfacePath(SurfacePoint(-40, 300), SurfacePoint(40, 60))
        self.assertTrue(pathsIntersect(path1, path2))

    def testPathsDontIntersectOnDateline(self):
        path1 = SurfacePath(SurfacePoint(40, 300), SurfacePoint(20, 60))
        path2 = SurfacePath(SurfacePoint(-40, 300), SurfacePoint(-20, 60))
        self.assertFalse(pathsIntersect(path1, path2))

    def testPathsDontIntersectFullMeridian(self):
        path1 = SurfacePath(SurfacePoint(-90, 0), SurfacePoint(88, 0))
        path2 = SurfacePath(SurfacePoint(70, 120), SurfacePoint(70, 240))
        self.assertFalse(pathsIntersect(path1, path2))

    def testPathsIntersectOnMeridianCrossDateline(self):
        path1 = SurfacePath(SurfacePoint(0, 300), SurfacePoint(0, 40))
        path2 = SurfacePath(SurfacePoint(-40, 0), SurfacePoint(40, 0))
        self.assertTrue(pathsIntersect(path1, path2))

    def testPathsIntersectCrossingPole(self):
        path1 = SurfacePath(SurfacePoint(70, 60), SurfacePoint(70, 240))
        path2 = SurfacePath(SurfacePoint(80, 59), SurfacePoint(80, 61))
        path3 = SurfacePath(SurfacePoint(80, 239), SurfacePoint(80, 241))
        path4 = SurfacePath(SurfacePoint(70, 240), SurfacePoint(70, 60))
        path5 = SurfacePath(SurfacePoint(-80, 60), SurfacePoint(-80, 240), long=True)
        path6 = SurfacePath(SurfacePoint(70, 60), SurfacePoint(70, 240), long=True)
        self.assertTrue(pathsIntersect(path1, path2))
        self.assertTrue(pathsIntersect(path1, path3))
        self.assertTrue(pathsIntersect(path2, path1))
        self.assertTrue(pathsIntersect(path3, path1))
        self.assertTrue(pathsIntersect(path4, path2))
        self.assertTrue(pathsIntersect(path4, path3))
        self.assertTrue(pathsIntersect(path5, path3))
        self.assertTrue(pathsIntersect(path3, path5))
        self.assertFalse(pathsIntersect(path6, path3))
        self.assertFalse(pathsIntersect(path2, path6))

    def testPathsIntersectCrossingBothPoles(self):
        path1 = SurfacePath(SurfacePoint(70, 60), SurfacePoint(-20, 60))
        path2 = SurfacePath(SurfacePoint(80, 59), SurfacePoint(80, 61))
        path3 = SurfacePath(SurfacePoint(-40, 239), SurfacePoint(-40, 241))
        path4 = SurfacePath(SurfacePoint(-30, 59), SurfacePoint(-30, 61))
        path5 = SurfacePath(SurfacePoint(70, 60), SurfacePoint(-20, 60), long=True)
        self.assertFalse(pathsIntersect(path2, path1))
        self.assertFalse(pathsIntersect(path3, path1))
        self.assertFalse(pathsIntersect(path4, path1))
        self.assertFalse(pathsIntersect(path1, path2))
        self.assertFalse(pathsIntersect(path1, path3))
        self.assertFalse(pathsIntersect(path1, path4))
        self.assertTrue(pathsIntersect(path2, path5))
        self.assertTrue(pathsIntersect(path3, path5))
        self.assertTrue(pathsIntersect(path4, path5))
        self.assertTrue(pathsIntersect(path5, path2))
        self.assertTrue(pathsIntersect(path5, path3))
        self.assertTrue(pathsIntersect(path5, path4))

    def testPathsDontIntersectCrossingBothPoles(self):
        path1 = SurfacePath(SurfacePoint(70, 60), SurfacePoint(-20, 60))
        path2 = SurfacePath(SurfacePoint(80, 57), SurfacePoint(80, 59))
        path3 = SurfacePath(SurfacePoint(-40, 237), SurfacePoint(-40, 239))
        path4 = SurfacePath(SurfacePoint(-30, 57), SurfacePoint(-30, 59))
        self.assertFalse(pathsIntersect(path2, path1))
        self.assertFalse(pathsIntersect(path3, path1))
        self.assertFalse(pathsIntersect(path4, path1))
        self.assertFalse(pathsIntersect(path1, path2))
        self.assertFalse(pathsIntersect(path1, path3))
        self.assertFalse(pathsIntersect(path1, path4))

    def testPathCrossingCorner(self):
        pathToAnchor = SurfacePath(SurfacePoint(-40, 300), SurfacePoint(40, 60))
        b1 = SurfacePath(SurfacePoint(0, 120), SurfacePoint(0, 0))
        b2 = SurfacePath(SurfacePoint(0, 0), SurfacePoint(70, 0))
        self.assertFalse(pathsIntersect(pathToAnchor, b1))
        self.assertTrue(pathsIntersect(pathToAnchor, b2))

    def testPathPolarCorner(self):
        pathToAnchor = SurfacePath(SurfacePoint(-88, 0), SurfacePoint(90, 0))
        b1 = SurfacePath(SurfacePoint(70, 0), SurfacePoint(70, 120))
        b2 = SurfacePath(SurfacePoint(70, 240), SurfacePoint(70, 0))
        self.assertTrue(pathsIntersect(pathToAnchor, b1))
        self.assertFalse(pathsIntersect(pathToAnchor, b2))

    # TODO
    # This edge case is a bug in my current geodetics engine. It arises because
    # we get some floating point error in my code to compute the intersections between
    # great circles used to determine whether two paths cross each other or not. This
    # is normally acceptable but shows up if a path happens to pass very close to the
    # vertex between two consecutive borders. In this case, the intersections computed
    # with their respective great circles should be identical since it is the same
    # point, but in this implementation they aren't due to the above FP error. This
    # means if we are unlucky, they will be shifted enough affect the hit test -
    # meaning a path could test as crossing both borders or neither, either of which
    # will give a wrong result when we want to use an odd number of crossings to denote
    # the point being outside a polygon.
    @unittest.expectedFailure
    def testBackDiagonalCornerFPError(self):
        pathToAnchor = SurfacePath(SurfacePoint(-40, 300), SurfacePoint(40, 180))
        b1 = SurfacePath(SurfacePoint(70, 240), SurfacePoint(0, 240))
        b2 = SurfacePath(SurfacePoint(0, 240), SurfacePoint(0, 120))
        self.assertFalse(pathsIntersect(pathToAnchor, b1))
        self.assertTrue(pathsIntersect(pathToAnchor, b2))

        # Negative - antipodes on neither arc /
        # Negative - antipodes on one are /
        # Edge cases
        # Crosses date line /
        # Works for either direction of path/
        # Crosses pole
        # Crosses south pole
        # Crosses both poles
        # Equatorial


class TestIntermediatePoint(unittest.TestCase):
    def setUp(self):
        self.p1 = SurfacePoint(0, 0)
        self.p2 = SurfacePoint(0, 60)
        self.p3 = SurfacePoint(-60, 0)
        self.p4 = SurfacePoint(0, -60)
        self.p5 = SurfacePoint(60, 0)

    def testIntermediatePoint(self):
        path12 = SurfacePath(self.p1, self.p2)
        path24 = SurfacePath(self.p2, self.p4)
        path35 = SurfacePath(self.p3, self.p5)
        self.assertTrue(almostEqual(path12.intermediatePoint(0.5), SurfacePoint(0, 30)))
        self.assertEqual(path24.intermediatePoint(0.5), path35.intermediatePoint(0.5))
