import json
import math

from planetsim.surfaceRegion import SurfaceRegion
from planetsim.surfacePath import SurfacePath
from planetsim.surfacePoint import SurfacePoint
from planetsim.surfaceObject import SurfaceObject
from planetsim.surfaceVehicle import SurfaceVehicle
from planetsim.surfaceBase import SurfaceBase
from planetsim.vehicle import Vehicle

from utility.fileLoad import loadEntityFile

EARTH_RADIUS = 6371000

class PlanetSurface:
    def __init__(self, jsonPath = "json/planets/surfaces/Surface.json", vehiclePath = None, radius = EARTH_RADIUS, vehicleClasses = {}, vehicleRegisterCallback = None):
        self.radius = radius
        self.vehicleClasses = vehicleClasses
        self.regions = {}
        self.points = {}
        self.pointIdGenerator = self.newPointId()
        jsonFile = open(jsonPath, "r")
        jsonNodes = json.load(jsonFile)

        self.id = jsonNodes["id"]
        self.planetClass = jsonNodes["class"]
        jsonRegions = jsonNodes["Regions"]

        for r in jsonRegions:
            anchor = SurfacePoint(r["anchor"][0], r["anchor"][1])
            vertices = r["edges"]
            borders = []
            for i in range(len(vertices)-1):
                p1 = vertices[i]
                p2 = vertices[i+1]
                borders.append(SurfacePath(SurfacePoint(p1[0], p1[1]), SurfacePoint(p2[0], p2[1])))
            p1 = vertices[-1]
            p2 = vertices[0]
            borders.append(SurfacePath(SurfacePoint(p1[0], p1[1]), SurfacePoint(p2[0], p2[1])))


            region = SurfaceRegion(r["id"], anchor, borders, name=r.get("name"), terrain=r.get("terrain"))
            self.regions[region.id] = region

        if vehiclePath:
            self.vehicles = loadEntityFile(vehiclePath, self.id, Vehicle)
        else:
            self.vehicles = {}
        ###TODO: See same thing in orbitSim for ship classes
        for vehicle in self.vehicles.values():
            vehicle.vehicleClass = self.vehicleClasses[vehicle.vehicleClass]
            if vehicleRegisterCallback:
                vehicleRegisterCallback(vehicle.id)

        jsonObjects = jsonNodes.get("Objects")

        if jsonObjects:
            for object in jsonObjects:
                pointArray = object["point"]
                point = SurfacePoint(pointArray[0], pointArray[1])
                if "colonyId" in object:
                    self.createBase(None, point, name = object["name"], colonyId = object["colonyId"])
                elif "vehicle" in object:
                    self.createVehicle(None, point, name = object["name"], payload = self.vehicles[object["vehicle"]])
                else:
                    self.createObject(None, point, name = object["name"])


        jsonFile.close()

    def newPointId(self):
        pointIdCounter = 0
        while True:
            yield pointIdCounter
            pointIdCounter += 1

    def gcDistance(self, path):
        return self.radius * path.gcAngle()

    def _angleForDistance(self, distance):
        return distance / self.radius

    def createObject(self, content, position, name=""):
        id = next(self.pointIdGenerator)
        self.points[id] = SurfaceObject(id, content, position, name = name)
        return id
    
    def createVehicle(self, content, position, name="", payload=None):
        id = next(self.pointIdGenerator)
        self.points[id] = SurfaceVehicle(id, content, position, payload = payload)
        if payload:
            self.vehicles[payload.id] = payload
        return id 

    def createBase(self, context, position, name="", colonyId = None):
        id = next(self.pointIdGenerator)
        self.points[id] = SurfaceBase(id, context, position, name = name, colonyId = colonyId)
        return id

    def destroyObject(self, id):
        self.points[id].kill()
        del self.points[id]

    def connectColony(self, colony):
        for point in self.points.values():
            if isinstance(point, SurfaceBase) and point.colonyId == colony.id:
                point.content = colony

    def transferVehicle(self, id):
        vehicle = self.vehicleById(id)
        for point in self.points.values():
            if isinstance(point, SurfaceVehicle) and point.payload == vehicle:
                self.destroyObject(point.id)
        del self.vehicles[id]
        return vehicle

    def regionForPointId(self, id):
        object = self.pointById(id)
        return self.regionForObject(object)

    def regionForObject(self, object):
        return self.regionForPoint(object.point)

    def regionForPoint(self, point):
        for r in self.regions.values():
            if r.pointInRegion(point):
                return r

        return None

    def _distanceForTime(self, id, time):
        point = self.pointById(id)
        return time * point.maxV()

    def tick(self, increment):
        purgeIds = set()
        for p in self.points.values():
            if isinstance(p, SurfaceVehicle) and p.destination:
                # First work out how far we can travel in this time
                maxDistance = self._distanceForTime(p.id, increment)
                path = SurfacePath(p.point, p.destination)
                remainingDistance = self.gcDistance(path)
                if (maxDistance >= remainingDistance):
                    distance = remainingDistance
                else:
                    distance = maxDistance

                # Now see how far fuel load will get us
                fuelBurn = p.fuelPerM() * distance
                if (fuelBurn <= p.payload.fuel):
                    p.payload.fuel -= fuelBurn
                else:
                    distance = p.payload.fuel / p.fuelPerM()
                    p.payload.fuel = 0

                # Now do the actual move
                if distance:
                    fraction = distance/remainingDistance
                else:
                    fraction = 0.0
                waypoint = path.intermediatePointTrig(fraction).canonical()
                p.point = waypoint
                    
                # Check if we've arrived and clear destination
                if math.isclose(p.point.latitude, p.destination.latitude) and math.isclose(p.point.longitude, p.destination.longitude):
                    p.setDestination(None)
                    for dp in self.objectsAtPoint(p.point):
                        if dp is p:
                            continue
                        terminal = dp.content.vehicleArrival(p.payload)
                        if (terminal):
                            purgeIds.add(p.id)
                            break

        for id in purgeIds:
            self.destroyObject(id)




        # For each point
        # If it has a destination,
        # Work out how far it would travel in this increment
        # Work out the total distance remaining.
        # If travel > remaining, point reaches destination
        # Otherwise, work out angle subtended by distance.
        # Work out point reached on path by moving this angle from start. (see resource on intermediate point)
        # Set point to this position.

    def objectsAtPoint(self, point):
        return tuple(p for p in self.points.values() if (math.isclose(p.point.longitude, point.longitude) and math.isclose(p.point.latitude, point.latitude)))

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
    
    def vehicleById(self, id):
        if not isinstance(id, int):
            raise TypeError
        elif id < 0:
            raise ValueError
        return self.vehicles[id]
    





