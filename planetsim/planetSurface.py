import json

from planetsim.surfaceRegion import SurfaceRegion
from planetsim.surfacePath import SurfacePath
from planetsim.surfacePoint import SurfacePoint, dot, cross, magnitude, latLong
import math

EARTH_RADIUS = 6371000

class PlanetSurface:
    def __init__(self, jsonPath = "json/Surface.json", radius = EARTH_RADIUS):
        self.radius = radius
        self.regions = []
        self.points = []
        jsonFile = open(jsonPath, "r")
        jsonTechs = json.load(jsonFile)

        jsonNodes = jsonTechs["Regions"]

        for r in jsonNodes:
            anchor = SurfacePoint(r["anchor"][0], r["anchor"][1])
            borders = []
            for b in r["edges"]:
                borders.append(SurfacePoint(b[0], b[1]))
            region = SurfaceRegion(r["id"], anchor, borders)
            self.regions.append(region)


    def gcDistance(self, path):
        return self.radius * path.gcAngle()
   


    def gcIntersections(self, path1, path2):
        gc1 = path1.gc()
        gc2 = path2.gc()
        i1 = cross(gc1, gc2)
        i2 = cross(gc2, gc1)
        return (i1, i2)

    # Convention on path handling:
    # We always assume the path travels eastward from p1 to p2. 
    # This should let us consistently specify paths including with dateline.
    # Special handling needed for meridianal paths - in this case always travel north from p1. 
    def pathsIntersect(self, path1, path2):
        intersections = tuple(latLong(i).normalise() for i in self.gcIntersections(path1, path2))
        intersect = False
        # If either path is on a meridian it won't describe a full 360 in longitude, so we  
        # can't use longitude to test intermediacy. 
        p1Meridian = path1.isMeridian()
        p2Meridian = path2.isMeridian()

        for i in intersections:
            pIntersect = [False, False]
            for index, path in enumerate((path1, path2)):
                if path.isMeridian():
                    if math.isclose(path.p1.longitude,path.p2.longitude):
                        # Path stays in a single meridian
                        if path.p1.latitude > path.p2.latitude:
                        #This is a transpolar path, crossing both north and south pole
                            if i.latitude > path.p1.latitude or i.latitude < path.p2.latitude:
                                pIntersect[index] = True
                        elif i.latitude > path.p1.latitude and i.latitude < path.p2.latitude:
                            pIntersect[index] = True
                    else:
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
