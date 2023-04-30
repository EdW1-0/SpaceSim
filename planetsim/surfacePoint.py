from dataclasses import dataclass
from math import cos, sin, pi, atan2, sqrt

def canonicalPoint(point):
    normlat = point.latitude
    normlong = point.longitude
    normlat = normlat % 360.0
    if normlat > 270.0:
        normlat -= 360.0
    elif normlat > 90.0:
        normlong += 180.0
        normlat = 180.0 - normlat

    normlong = normlong % 360.0
    return SurfacePoint(normlat, normlong)

def dot(v1, v2):
    return sum([v1[i]*v2[i] for i in range(3)])

def cross(v1, v2):
    return (v1[1]*v2[2]-v1[2]*v2[1], v1[2]*v2[0]-v1[0]*v2[2], v1[0]*v2[1] - v1[1]*v2[0])

def magnitude(v1):
    return sqrt(sum([v1[i]**2 for i in range(3)]))

def normalise(v):
    m = magnitude(v)
    return tuple(vi/m for vi in v)

def pointFromVector(v):
    ll = latLong(v)
    return SurfacePoint(ll[0], ll[1])

def latLong(v):
    lat = atan2(v[2], sqrt(v[0]**2 + v[1]**2))
    long = atan2(v[1], v[0])
    long = long % (2*pi)
    return (lat*180.0/pi, long*180.0/pi)


def almostEqual(p1, p2, debug=False):
    latTest = abs(p1.latitude - p2.latitude) < 0.01
    longTest = abs(p1.longitude - p2.longitude) < 0.01
    if debug and not (latTest and longTest):
        print (p1, " is not ", p2)

    return latTest and longTest

def vector(lat, long):
    latr = lat / 180 * pi
    longr = long / 180 * pi
    x = cos(latr)*cos(longr)
    y = cos(latr)*sin(longr)
    z = sin(latr)
    return (x, y, z)

@dataclass
class SurfacePoint:
    latitude: float
    longitude: float

    def vector(self):
        return vector(self.latitude, self.longitude)

    def canonical(self):
        return canonicalPoint(self)
    
    def __str__(self):
        return "({0:.2f}, {1:.2f})".format(self.latitude, self.longitude)

