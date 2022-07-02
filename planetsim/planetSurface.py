import json

from planetsim.surfaceRegion import SurfaceRegion
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

    def gcAngle(self, point1, point2):
        sine = magnitude(cross(point1.vector(), point2.vector()))
        cosine = dot(point1.vector(), point2.vector())
        return math.atan2(sine, cosine)

    def gcAngleHav(self, point1, point2):
        phi1 = point1.latitude * math.pi/180.0
        phi2 = point2.latitude * math.pi/180.0
        deltaphi = (point2.latitude - point1.latitude) * math.pi/180.0
        deltalambda = (point2.longitude - point1.longitude) * math.pi/180.0
        a = math.sin(deltaphi/2)*math.sin(deltaphi/2) + math.cos(phi1)*math.cos(phi2) + math.sin(deltalambda/2)*math.sin(deltalambda/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return c

    def gcDistance(self, point1, point2):
        return self.radius * self.gcAngle(point1, point2)
   
    def gc(self, path):
        v1 = path[0].vector()
        v2 = path[1].vector()
        c = cross(v1, v2)
        mag = magnitude(c)
        gc = tuple(i/mag for i in c)
        return gc

    def gcIntersections(self, path1, path2):
        gc1 = self.gc(path1)
        gc2 = self.gc(path2)
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
        p1Meridian = path1[0].longitude % 180.0 == path1[1].longitude % 180.0
        p2Meridian = path2[0].longitude % 180.0 == path2[1].longitude % 180.0
        for i in intersections:
            p1Intersect = False
            p2Intersect = False
            if p1Meridian:
                if math.isclose(path1[0].longitude,path1[1].longitude):
                    # Path stays in a single meridian
                    if i.latitude > path1[0].latitude and i.latitude < path1[1].latitude:
                        p1Intersect = True
                else:
                    # Path crosses a pole
                    # Currently no way of handling south polar paths
                    if math.isclose(i.longitude, path1[0].longitude) and i.latitude > path1[0].latitude:
                        p1Intersect = True
                    elif math.isclose(i.longitude, path1[1].longitude) and i.latitude > path1[1].latitude:
                        p1Intersect = True
            elif path1[0].longitude > path1[1].longitude: 
                # path crosses dateline so test if p1.lo < long < 360 or 0 < long < p2.lo
                if i.longitude > path1[0].longitude or i.longitude < path1[1].longitude:
                    p1Intersect = True
            elif i.longitude > path1[0].longitude and i.longitude < path1[1].longitude:
                p1Intersect = True

            if p2Meridian:
                if math.isclose(path2[0].longitude, path2[1].longitude):
                    if i.latitude > path2[0].latitude and i.latitude < path2[1].latitude:
                        p2Intersect = True
                else:
                    # Path crosses a pole
                    # Currently no way of handling south polar paths
                    if math.isclose(i.longitude, path2[0].longitude) and i.latitude > path2[0].latitude:
                        p1Intersect = True
                    elif math.isclose(i.longitude, path2[1].longitude) and i.latitude > path2[1].latitude:
                        p1Intersect = True
            elif path2[0].longitude > path2[1].longitude:
                if i.longitude > path2[0].longitude or i.longitude < path2[1].longitude:
                    p2Intersect = True
            elif i.longitude > path2[0].longitude and i.longitude < path2[1].longitude:
                p2Intersect = True

            if p1Intersect and p2Intersect:
                intersect = True

        return intersect

