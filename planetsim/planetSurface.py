import json

class PlanetSurface:
    def __init__(self, jsonPath = "json/Surface.json"):
        jsonFile = open(jsonPath, "r")
        jsonTechs = json.load(jsonFile)

        self.regions = []
        self.points = []