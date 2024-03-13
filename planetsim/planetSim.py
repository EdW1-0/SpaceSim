import json
import os

from planetsim.planet import Planet
from planetsim.planetSurface import PlanetSurface
from planetsim.planetTerrain import PlanetTerrain
from planetsim.vehicleClass import VehicleClass
from planetsim.vehicle import Vehicle
from planetsim.surfacePoint import SurfacePoint
from planetsim.surfaceBase import SurfaceBase

from utility.fileLoad import loadEntityFile
from utility.dictLookup import getStringId
from utility.idGenerator import IDGenerator

from playerState import PlayerState


class PlanetSim:
    def __init__(
        self,
        orbitSim,
        playerState: PlayerState = None,
        jsonPath="json/Planets.json",
        vehicleClassPath="json/vehicleClasses",
        vehiclePath="json/vehicles",
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
                vehicleClassPath, "VehicleClasses", VehicleClass, playerState=playerState
            )
        else:
            self.vehicleClasses = {}

        self.vehicleIdGenerator = IDGenerator()
        self._vehicleIds = set()

        if vehiclePath:
            self.vehicles = loadEntityFile(vehiclePath, "Vehicles", Vehicle)
        else:
            self.vehicles = {}
        # TODO: See same thing in orbitSim for ship classes
        for vehicle in self.vehicles.values():
            vehicle.vehicleClass = self.vehicleClasses[vehicle.vehicleClass]
            self.vehicleIdGenerator.setId(vehicle.id)

        surfacesFolder = "json/planets/surfaces/"

        for subdir, dirs, files in os.walk(surfacesFolder):
            for file in files:
                surface = PlanetSurface(
                    orbitSim,
                    surfacesFolder + file,
                    radius=1000,
                    vehicleAccessor=self.vehicleById
                )
                for planetId in self.planets.keys():
                    if planetId == surface.id:
                        # TODO: Bit of a kludge to set this later when it should go
                        # in via constructor. Should load all these first, then call
                        # constructor
                        self.planets[planetId].surface = surface



    def createVehicle(self, name, vehicleClass, fuel=0):
        id = self.vehicleIdGenerator.generateId()
        while id in self.vehicles:
            id = next(self.vehicleIdGenerator)
        self.vehicles[id] = Vehicle(id, name, vehicleClass, fuel=fuel)
        return id


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

    def vehicleById(self, id):
        return getStringId(id, self.vehicles)

    def tick(self, increment):
        for planet in self.planets.values():
            planet.tick(increment)
