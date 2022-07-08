from dataclasses import dataclass
import math

from planetsim.surfacePoint import SurfacePoint, magnitude, dot, cross, latLong

# Encodes an arc on a great circle path as a pair of points. 
# By convention is the shortest GC path between them, unless long is set in which case it is the 
# reverse (long) path that is taken.
# For antipodes the choice of path is ambiguous. In this case we follow a convention:
# "Short" path is the path travelling east from p1.
# If path is on a meridian, then "short" path is northwards. 

@dataclass
class SurfacePath:
    p1: SurfacePoint = SurfacePoint(0,0)
    p2: SurfacePoint = SurfacePoint(0,0) 
    long: bool = False

    def gcAngle(self):
        sine = magnitude(cross(self.p1.vector(), self.p2.vector()))
        cosine = dot(self.p1.vector(), self.p2.vector())
        return math.atan2(sine, cosine)

    def gc(self):
        v1 = self.p1.vector()
        v2 = self.p2.vector()
        c = cross(v1, v2)
        mag = magnitude(c)
        gc = tuple(i/mag for i in c)
        return gc

    def isMeridian(self):
        return self.p1.longitude % 180.0 == self.p2.longitude % 180.0

    def crossesDateline(self):
        if abs(self.p1.longitude - self.p2.longitude) < 180.0:
            return self.long
        else:
            return not self.long

    def isNorthPolar(self):
        if not self.isMeridian():
            return False

        if self.p1.longitude == self.p2.longitude:
            return False

        # >= is important - convention if equidistant north/south to cross north pole.
        if not self.long:
            return (self.p1.latitude + self.p2.latitude >= 0.0)
        else:
            return (self.p1.latitude + self.p2.latitude <= 0.0)

    def isSouthPolar(self):
        if not self.isMeridian():
            return False

        if self.p1.longitude == self.p2.longitude:
            return False

        return not self.isNorthPolar()

    def isDoublePolar(self):
        if not self.isMeridian():
            return False

        if self.p1.longitude == self.p2.longitude:
            return self.long
        else:
            return False

    # Tests if a given great circle point falls within the arc described on the GC by this path.
    # IMPORTANT: Does *NOT* test whether point falls on the great circle in the first place. It assumes it 
    # does, and given that, just checks whether it falls on the arc between these points or the arc
    # outside it. 
    # Testing with a point not on the great circle will give unpredictable and probably wrong results!
    def pointOnPath(self, point):
        if self.p1.longitude > self.p2.longitude: 
                # path crosses dateline so test if p1.lo < long < 360 or 0 < long < p2.lo
            if point.longitude > self.p1.longitude or point.longitude < self.p2.longitude:
                return True
        else:
            return point.longitude > self.p1.longitude and point.longitude < self.p2.longitude




def gcIntersections(path1, path2):
    gc1 = path1.gc()
    gc2 = path2.gc()
    i1 = cross(gc1, gc2)
    i2 = cross(gc2, gc1)
    return (i1, i2)

# Convention on path handling:
 # We always assume the path travels on the shortest GC, unless long is specified. 
 # This should let us consistently specify paths including with dateline.
 # If path is equidistant, convention should be to take East/North route. 
def pathsIntersect(path1, path2):
    intersections = tuple(latLong(i).normalise() for i in gcIntersections(path1, path2))
    intersect = False
    # If either path is on a meridian it won't describe a full 360 in longitude, so we  
    # can't use longitude to test intermediacy. 
    p1Meridian = path1.isMeridian()
    p2Meridian = path2.isMeridian()

    for i in intersections:
        pIntersect = [False, False]
        for index, path in enumerate((path1, path2)):
            if path.isMeridian():
                # Meridianal paths don't describe a full 360 in longitude so need special handling
                if math.isclose(path.p1.longitude,path.p2.longitude):
                    # Path stays in a single meridian or else loops around both poles
                    if path.isDoublePolar():
                        if not isIntermediate(i.latitude, (path.p1.latitude, path.p2.latitude)):
                            pIntersect[index] = True
                    elif isIntermediate(i.latitude, (path.p1.latitude, path.p2.latitude)):
                        pIntersect[index] = True
                else:
                    # Path crosses a single pole, so figure out which hemisphere i is in and then test each pole
                    for p in (path.p1, path.p2):
                        if math.isclose(i.longitude, p.longitude):
                            if path.isNorthPolar() and i.latitude > p.latitude:
                                pIntersect[index] = True
                            elif path.isSouthPolar() and i.latitude < p.latitude:
                                pIntersect[index] = True
            elif path.crossesDateline(): 
            # path crosses dateline so test if p1.lo < long < 360 or 0 < long < p2.lo
                if not isIntermediate(i.longitude, (path.p1.longitude, path.p2.longitude)):
                    pIntersect[index] = True
            elif isIntermediate(i.longitude, (path.p1.longitude, path.p2.longitude)):
                # path is on a longitudinal great circle and doesn't cross the dateline, so a simple check 
                # longitude is intermediate
                pIntersect[index] = True

        intersect = pIntersect[0] and pIntersect[1]
        if intersect:
            break

    return intersect


def isIntermediate(value, range):
    if range[0] > range[1]:
        if value < range[0] and value > range[1]:
            return True
        else:
            return False
    else:
        if value > range[0] and value < range[1]:
            return True
        else:
            return False
        