from colonysim.building import Building
from colonysim.buildingClass import BuildingClass

class Colony:
    def __init__(self, id, name, ships = {}, vehicles = {}):
        self.id = id
        self.name = name
        self.ships = ships
        self.vehicles = vehicles
        self.buildings = {}
        self.buildingIdGenerator = self.newBuildingId()

    def newBuildingId(self):
        nodeIdCounter = 0
        while True:
            yield nodeIdCounter
            nodeIdCounter += 1


    # Question over whether this should be given a buildingClass reference directly, or just an id and look it up from colonySim.
    # I think this should be OK even though we will proliferate refs to buildingClass instances - these should all be singleton objects
    # with lifespan equal to the life of the game instance anyway, and this saves an extra lookup through colonysim. 
    def addBuilding(self, buildingClass):
        id = next(self.buildingIdGenerator)
        self.buildings[id] = Building(id, buildingClass)
        return id
