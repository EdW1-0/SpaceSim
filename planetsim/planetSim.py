import json
import os

from planetsim.planet import Planet
from planetsim.planetSurface import PlanetSurface

class PlanetSim:
    def __init__(self, jsonPath = "json/Planets.json"):
        jsonFile = open(jsonPath, "r")
        jsonPlanets = json.load(jsonFile)

        jsonNodes = jsonPlanets["Planets"]

        self.planets = {node["id"]: Planet(**node) for node in jsonNodes}
        jsonFile.close()



        surfacesFolder = 'json/planets/surfaces/'

        for subdir, dirs, files in os.walk(surfacesFolder):
            for file in files:
                surface = PlanetSurface(surfacesFolder + file, 1000)
                for planetId in self.planets.keys():
                    if planetId == surface.id:
                        ###TODO: Bit of a kludge to set this later when it should go in via constructor. Should load all these first, then call constructor
                        self.planets[planetId].surface = surface


    def planetById(self, id):
        if not (type(id) == int or isinstance(id, str)):
            raise TypeError
        elif isinstance(id, str) and not id.isupper():
            raise ValueError
        return self.planets[id]
    
    def tick(self, increment):
        pass

