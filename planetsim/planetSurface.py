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

    def createObject(self, content, position):
        id = next(self.pointIdGenerator)
        self.points[id] = SurfaceObject(id, content, position)

    def destroyObject(self, id):
        del self.points[id]


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





