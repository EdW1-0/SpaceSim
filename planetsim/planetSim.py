import json
import os

from planetsim.planet import Planet
from planetsim.planetSurface import PlanetSurface
from planetsim.planetTerrain import PlanetTerrain

class PlanetSim:
    def __init__(self, jsonPath = "json/Planets.json"):
        planetsFile = open(jsonPath, "r")
        planetsJson = json.load(planetsFile)

        planets = planetsJson["Planets"]

        self.planets = {planet["id"]: Planet(**planet) for planet in planets}
        planetsFile.close()


        classesFolder = 'json/planets/classes/'

        self.planetClasses = {}
        for subdir, dirs, files in os.walk(classesFolder):
            for file in files:
                classFile = open(classesFolder + file, "r")
                classJson = json.load(classFile)
                classId = classJson["id"]
                self.planetClasses[classId] = {}
                terrainTypes = classJson["Terrain"]
                self.planetClasses[classId] = {terrain["id"]: PlanetTerrain(**terrain) for terrain in terrainTypes}
                classFile.close()


        surfacesFolder = 'json/planets/surfaces/'

        for subdir, dirs, files in os.walk(surfacesFolder):
            for file in files:
                surface = PlanetSurface(surfacesFolder + file, 1000)
                for planetId in self.planets.keys():
                    if planetId == surface.id:
                        ###TODO: Bit of a kludge to set this later when it should go in via constructor. Should load all these first, then call constructor
                        self.planets[planetId].surface = surface



    def planetClassById(self, id):
        if not (type(id) == int or isinstance(id, str)):
            raise TypeError
        elif isinstance(id, str) and not id.isupper():
            raise ValueError
        return self.planetClasses[id]


    def planetById(self, id):
        if not (type(id) == int or isinstance(id, str)):
            raise TypeError
        elif isinstance(id, str) and not id.isupper():
            raise ValueError
        return self.planets[id]
    
    def tick(self, increment):
        pass

