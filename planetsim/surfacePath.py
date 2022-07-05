from dataclasses import dataclass
import math

from planetsim.surfacePoint import SurfacePoint, magnitude, dot, cross

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
        
