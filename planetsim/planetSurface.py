import json

from planetsim.surfaceRegion import SurfaceRegion
from planetsim.surfacePath import SurfacePath
from planetsim.surfacePoint import SurfacePoint
from planetsim.surfaceObject import SurfaceObject
from planetsim.surfaceVehicle import SurfaceVehicle
from planetsim.surfaceBase import SurfaceBase

EARTH_RADIUS = 6371000

class PlanetSurface:
    def __init__(self, jsonPath = "json/planets/surfaces/Surface.json", radius = EARTH_RADIUS):
        self.radius = radius
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


        jsonObjects = jsonNodes.get("Objects")

        if jsonObjects:
            for object in jsonObjects:
                pointArray = object["point"]
                point = SurfacePoint(pointArray[0], pointArray[1])
                if "colonyId" in object:
                    self.createBase(None, point, name = object["name"], colonyId = object["colonyId"])
                elif "fuel" in object:
                    self.createVehicle(None, point, name = object["name"], fuel = object["fuel"], maxV = object["maxV"], fuelPerM = object["fuelPerM"])
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
    
    def createVehicle(self, content, position, name="", fuel = 0, maxV = 0, fuelPerM = 0):
        id = next(self.pointIdGenerator)
        self.points[id] = SurfaceVehicle(id, content, position, name = name, fuel=fuel, maxV=maxV, fuelPerM=fuelPerM)
        return id

    def createBase(self, context, position, name="", colonyId = None):
        id = next(self.pointIdGenerator)
        self.points[id] = SurfaceBase(id, context, position, name = name, colonyId = colonyId)
        return id

    def destroyObject(self, id):
        del self.points[id]

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
        return time * point.maxV

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
                fuelBurn = p.fuelPerM * distance
                if (fuelBurn <= p.fuel):
                    p.fuel -= fuelBurn
                else:
                    distance = p.fuel / p.fuelPerM
                    p.fuel = 0

                # Now do the actual move
                if distance:
                    fraction = distance/remainingDistance
                else:
                    fraction = 0.0
                waypoint = path.intermediatePointTrig(fraction).canonical()
                p.point = waypoint
                    
                # Check if we've arrived and clear destination
                if p.point == p.destination:
                    p.setDestination(None)
                    for dp in self.objectsAtPoint(p.point):
                        if dp is p:
                            continue
                        terminal = dp.content.vehicleArrival(p.content)
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
        return tuple(p for p in self.points.values() if p.point == point)

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





