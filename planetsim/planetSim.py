import json
import os

from planetsim.planet import Planet
from planetsim.planetSurface import PlanetSurface
from planetsim.planetTerrain import PlanetTerrain
from planetsim.vehicleClass import VehicleClass
from planetsim.surfacePoint import SurfacePoint
from planetsim.surfaceBase import SurfaceBase

from utility.fileLoad import loadEntityFile
from utility.dictLookup import getStringId


class PlanetSim:
    def __init__(
        self,
        orbitSim,
        jsonPath="json/Planets.json",
        vehicleClassPath="json/vehicleClasses",
        vehicleRegisterCallback=None,
    ):
        planetsFile = open(jsonPath, "r")
        planetsJson = json.load(planetsFile)

        planets = planetsJson["Planets"]

        self.planets = {planet["id"]: Planet(**planet) for planet in planets}
        planetsFile.close()

        classesFolder = "json/planets/classes/"

        self.planetClasses = {}
        for subdir, dirs, files in os.walk(classesFolder):
            for file in files:
                classFile = open(classesFolder + file, "r")
                classJson = json.load(classFile)
                classId = classJson["id"]
                self.planetClasses[classId] = {}
                terrainTypes = classJson["Terrain"]
                self.planetClasses[classId] = {
                    terrain["id"]: PlanetTerrain(**terrain) for terrain in terrainTypes
                }
                classFile.close()
        if vehicleClassPath:
            self.vehicleClasses = loadEntityFile(
                vehicleClassPath, "VehicleClasses", VehicleClass
            )
        else:
            self.vehicleClasses = {}

        surfacesFolder = "json/planets/surfaces/"

        for subdir, dirs, files in os.walk(surfacesFolder):
            for file in files:
                surface = PlanetSurface(
                    orbitSim,
                    surfacesFolder + file,
                    radius=1000,
                    vehiclePath="json/planets/vehicles",
                    vehicleClasses=self.vehicleClasses,
                    vehicleRegisterCallback=vehicleRegisterCallback,
                )
                for planetId in self.planets.keys():
                    if planetId == surface.id:
                        # TODO: Bit of a kludge to set this later when it should go
                        # in via constructor. Should load all these first, then call
                        # constructor
                        self.planets[planetId].surface = surface

    def landShip(self, ship, planet, surfaceCoordinates):
        planet = self.planetById(planet)
        surface = planet.surface
        if isinstance(surfaceCoordinates, SurfacePoint):
            surface.createObject(ship, surfaceCoordinates, ship.name)
            ship.locale = surface
            return False
        elif isinstance(surfaceCoordinates, SurfaceBase):
            return surfaceCoordinates.content.shipArrival(ship)
        else:
            print("unrecognised surface coordinates type: ", surfaceCoordinates)
            assert False

    def planetClassById(self, id):
        return getStringId(id, self.planetClasses)

    def planetById(self, id):
        return getStringId(id, self.planets)
    
    def vehicleClassById(self, id):
        return getStringId(id, self.vehicleClasses)

    def tick(self, increment):
        for planet in self.planets.values():
            planet.tick(increment)
