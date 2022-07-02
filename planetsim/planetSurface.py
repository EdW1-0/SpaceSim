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
        p1Meridian = path1.p1.longitude % 180.0 == path1.p2.longitude % 180.0
        p2Meridian = path2.p1.longitude % 180.0 == path2.p2.longitude % 180.0
        for i in intersections:
            p1Intersect = False
            p2Intersect = False
            if p1Meridian:
                if math.isclose(path1.p1.longitude,path1.p2.longitude):
                    # Path stays in a single meridian
                    if path1.p1.latitude > path1.p2.latitude:
                        #This is a transpolar path, crossing both north and south pole
                        if i.latitude > path1.p1.latitude or i.latitude < path1.p2.latitude:
                            p1Intersect = True
                    elif i.latitude > path1.p1.latitude and i.latitude < path1.p2.latitude:
                        p1Intersect = True
                else:
                    # Path crosses a pole
                    # Currently no way of handling south polar paths
                    if math.isclose(i.longitude, path1.p1.longitude) and i.latitude > path1.p1.latitude:
                        p1Intersect = True
                    elif math.isclose(i.longitude, path1.p2.longitude) and i.latitude > path1.p2.latitude:
                        p1Intersect = True
            elif path1.p1.longitude > path1.p2.longitude: 
                # path crosses dateline so test if p1.lo < long < 360 or 0 < long < p2.lo
                if i.longitude > path1.p1.longitude or i.longitude < path1.p2.longitude:
                    p1Intersect = True
            elif i.longitude > path1.p1.longitude and i.longitude < path1.p2.longitude:
                p1Intersect = True

            if p2Meridian:
                if math.isclose(path2.p1.longitude, path2.p2.longitude):
                    if path2.p1.latitude > path2.p2.latitude:
                        #This is a transpolar path, crossing both north and south pole
                        if i.latitude > path2.p1.latitude or i.latitude < path2.p2.latitude:
                            p2Intersect = True
                    elif i.latitude > path2.p1.latitude and i.latitude < path2.p2.latitude:
                        p2Intersect = True
                else:
                    # Path crosses a pole
                    # Currently no way of handling south polar paths
                    if math.isclose(i.longitude, path2.p1.longitude) and i.latitude > path2.p1.latitude:
                        p2Intersect = True
                    elif math.isclose(i.longitude, path2.p2.longitude) and i.latitude > path2.p2.latitude:
                        p2Intersect = True
            elif path2.p1.longitude > path2.p2.longitude:
                if i.longitude > path2.p1.longitude or i.longitude < path2.p2.longitude:
                    p2Intersect = True
            elif i.longitude > path2.p1.longitude and i.longitude < path2.p2.longitude:
                p2Intersect = True

            if p1Intersect and p2Intersect:
                intersect = True

        return intersect

