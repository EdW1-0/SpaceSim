from dataclasses import dataclass
from math import cos, sin, pi

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
