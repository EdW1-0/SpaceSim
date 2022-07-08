import json

from planetsim.surfaceRegion import SurfaceRegion
from planetsim.surfacePath import SurfacePath
from planetsim.surfacePoint import SurfacePoint
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
            self.regions.append(region)


    def gcDistance(self, path):
        return self.radius * path.gcAngle()
   





