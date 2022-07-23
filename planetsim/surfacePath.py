from dataclasses import dataclass
import math

from planetsim.surfacePoint import SurfacePoint, magnitude, dot, cross, latLong, normalise

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
        # Special case of degenerate path - divideb by zero, so arbitrarily set this to a meridian.
        if self.p1 == self.p2:
            gc = normalise((-v1[1], v1[0], 0.0))
        else:
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

    def intermediatePoint(self, fraction):
        v1 = self.p1.vector()
        v2 = self.p2.vector()
        v1scale = tuple(vi*(1-fraction) for vi in v1)
        v2scale = tuple(vi*fraction for vi in v2)
        m = tuple(v1i+v2i for v1i, v2i in zip(v1scale, v2scale))
        mNorm = normalise(m)
        return latLong(mNorm)


#
#Formula:	a = sin((1−f)⋅δ) / sin δ
#b = sin(f⋅δ) / sin δ
#x = a ⋅ cos φ1 ⋅ cos λ1 + b ⋅ cos φ2 ⋅ cos λ2
#y = a ⋅ cos φ1 ⋅ sin λ1 + b ⋅ cos φ2 ⋅ sin λ2
#z = a ⋅ sin φ1 + b ⋅ sin φ2
#φi = atan2(z, √x² + y²)
#λi = atan2(y, x)
#where	f is fraction along great circle route (f=0 is point 1, f=1 is point 2), δ is the angular distance d/R between the two points.
    def intermediatePointTrig(self, fraction):
        d = self.gcAngle()
        
        a = math.sin((1-fraction)*d)/math.sin(d)
        b = math.sin(fraction*d)/math.sin(d)
        p1latR = self.p1.latitude * math.pi / 180
        p2latR = self.p2.latitude * math.pi / 180
        p1longR = self.p1.longitude * math.pi / 180
        p2longR = self.p2.longitude * math.pi / 180
        x = a*math.cos(p1latR)*math.cos(p1longR) + b*math.cos(p2latR)*math.cos(p2longR)
        y = a*math.cos(p1latR)*math.sin(p1longR) + b*math.cos(p2latR)*math.sin(p2longR)
        z = a*math.sin(p1latR) + b*math.sin(p2latR)
        latiR = math.atan2(z, math.sqrt(x**2 + y**2))
        longiR = math.atan2(y, x)
        lati = latiR * 180 / math.pi
        longi = longiR * 180 / math.pi
        return SurfacePoint(lati, longi)




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
    intersections = tuple(latLong(i).canonical() for i in gcIntersections(path1, path2))
    intersect = False

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
                    # Single hemisphere, so check it's the same hemisphere.
                    elif math.isclose(path.p1.longitude, i.longitude):
                        # If it is, check if the latitude is on the arc.
                        if isIntermediate(i.latitude, (path.p1.latitude, path.p2.latitude)):
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
                if not isIntermediate(i.longitude, (path.p2.longitude, path.p1.longitude)):
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
        if value <= range[0] and value > range[1]:
            return True
        else:
            return False
    else:
        if value >= range[0] and value < range[1]:
            return True
        else:
            return False
        
