from dataclasses import dataclass
from math import cos, sin, pi, atan2, sqrt

def normalisePoint(point):
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

def latLong(v):
    lat = atan2(v[2], sqrt(v[0]**2 + v[1]**2))
    long = atan2(v[1], v[0])
    return SurfacePoint(lat*180.0/pi, long*180.0/pi)

@dataclass
class SurfacePoint:
    latitude: float
    longitude: float

    def vector(self):
        latr = self.latitude / 180 * pi
        longr = self.longitude / 180 * pi
        x = cos(latr)*cos(longr)
        y = cos(latr)*sin(longr)
        z = sin(latr)
        return (x, y, z)
