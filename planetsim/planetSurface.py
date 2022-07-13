import json

from planetsim.surfaceRegion import SurfaceRegion
from planetsim.surfacePath import SurfacePath
from planetsim.surfacePoint import SurfacePoint
from planetsim.surfaceObject import SurfaceObject

EARTH_RADIUS = 6371000

class PlanetSurface:
    def __init__(self, jsonPath = "json/Surface.json", radius = EARTH_RADIUS):
        self.radius = radius
        self.regions = {}
        self.points = {}
        self.pointIdGenerator = self.newPointId()
        jsonFile = open(jsonPath, "r")
        jsonTechs = json.load(jsonFile)

        jsonNodes = jsonTechs["Regions"]

        for r in jsonNodes:
            anchor = SurfacePoint(r["anchor"][0], r["anchor"][1])
            vertices = r["edges"]
            borders = []
            for i in range(len(vertices)-1):
                p1 = vertices[i]
                p2 = vertices[i+1]
                borders.append(SurfacePath(SurfacePoint(p1[0], p1[1]), SurfacePoint(p2[0], p2[1])))
            p1 = vertices[-i]
            p2 = vertices[0]
            borders.append(SurfacePath(SurfacePoint(p1[0], p1[1]), SurfacePoint(p2[0], p2[1])))

            region = SurfaceRegion(r["id"], anchor, borders)
            self.regions[region.id] = region

    def newPointId(self):
        pointIdCounter = 0
        while True:
            yield pointIdCounter
            pointIdCounter += 1

    def gcDistance(self, path):
        return self.radius * path.gcAngle()

    def _angleForDistance(self, distance):
        return distance / self.radius

    def createObject(self, content, position):
        id = next(self.pointIdGenerator)
        self.points[id] = SurfaceObject(id, content, position)

    def destroyObject(self, id):
        del self.points[id]

    def _distanceForTime(self, id, time):
        point = self.pointById(id)
        return time * point.maxV

    def tick(self, increment):
        for p in self.points.values():
            if p.destination:
                distance = self._distanceForTime(p.id, increment)
                path = SurfacePath(p.point, p.destination)
                remainingDistance = self.gcDistance(path)
                if (distance >= remainingDistance):
                    p.point = p.destination
                    p.setDestination(None)
                else:
                    fraction = distance/remainingDistance
                    waypoint = path.intermediatePoint(fraction)
                    p.point = waypoint


        # For each point
        # If it has a destination,
        # Work out how far it would travel in this increment
        # Work out the total distance remaining.
        # If travel > remaining, point reaches destination
        # Otherwise, work out angle subtended by distance.
        # Work out point reached on path by moving this angle from start. (see resource on intermediate point)
        # Set point to this position.

    def regionById(self, id):
        if not isinstance(id, int):
            raise TypeError
        elif id < 0:
            raise ValueError
        return self.regions[id]

    def pointById(self, id):
        if not isinstance(id, int):
            raise TypeError
        elif id < 0:
            raise ValueError
        return self.points[id]





