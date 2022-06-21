import json

from planetsim.surfaceRegion import SurfaceRegion
from planetsim.surfacePoint import SurfacePoint

class PlanetSurface:
    def __init__(self, jsonPath = "json/Surface.json"):
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


