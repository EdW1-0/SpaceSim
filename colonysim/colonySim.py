import os
import json

from colonysim.resource import Resource
from colonysim.reaction import Reaction
from colonysim.buildingClass import BuildingClass, ProductionBuildingClass, StorageBuildingClass, ExtractionBuildingClass
from colonysim.building import Building, ProductionBuilding, StorageBuilding, ExtractionBuilding 
from colonysim.colony import Colony
from colonysim.productionOrder import ProductionOrder

from utility.fileLoad import loadEntityFile, extractEntityJson
from utility.dictLookup import getIntId, getStringId

class ColonySim:
    def __init__(self, orbitSim = None, planetSim = None, colonyPath = "json/colonies", resourcePath = "json/resources", reactionPath = "json/reactions", buildingPath = "json/buildingClasses"):
        self._buildingClasses = {}
        self._resources = {}
        self._reactions = {}

        self.idGenerator = self.newColonyId()
        self._colonies = {}

        self._resources = loadEntityFile(resourcePath, "Resources", Resource)

        self._reactions = loadEntityFile(reactionPath, "Reactions", Reaction)

        self._buildingClasses = loadEntityFile(buildingPath, 
                                                    "Buildings", 
                                                    BuildingClass, 
                                                    {
                                                        "reactions": ProductionBuildingClass,
                                                        "stores": StorageBuildingClass,
                                                        "extracts": ExtractionBuildingClass
                                                        })
        
        self._colonies = {}
        for subdir, dirs, files in os.walk(colonyPath):
            for file in files:
                colonyFile = open(colonyPath + "/" + file, "r")
                colonyJson = json.load(colonyFile)
                colonyFile.close()
                for planetId in colonyJson:
                    for c in colonyJson[planetId]:
                        id = c["id"]
                        name = c["name"]
                        surface = planetSim.planetById(planetId).surface
                        ships = c["ships"]
                        vehicles = c["vehicles"]

                        buildings = {}
                        for b in c["buildings"]:
                            bc = self.buildingClassById(b["buildingClass"])
                            if isinstance(bc, ProductionBuildingClass):
                                building = ProductionBuilding(b["id"], bc, self)
                                building.setReaction(b["reaction"])
                            elif isinstance(bc, StorageBuildingClass):
                                building = StorageBuilding(b["id"], bc)
                                building.setContents(b["contents"])
                                building.amount = b["amount"]
                            elif isinstance(bc, ExtractionBuildingClass):
                                building = ExtractionBuilding(b["id"], bc)
                            else:
                                building = Building(b["id"], bc)
                            if "constructionProgress" in b:
                                building.constructionProgress = b["constructionProgress"]
                            if "demolitionProgress" in b:
                                building.demolitionProgress = b["demolitionProgress"]
                            if "status" in b:
                                if b["status"] != "CONSTRUCTION":
                                    building.construct()
                                if b["status"] == "ACTIVE":
                                    building.start()
                                if b["status"] == "DEMOLITION":
                                    building.demolish()
                            else:
                                building.construct()

                            buildings[b["id"]] = building

                        productionOrders = {}
                        for po in c["productionOrders"]:
                            po["reaction"] = self.reactionById(po["reaction"])
                            status = po["status"]
                            del po["status"]
                            production = ProductionOrder(**po)
                            if status != "PENDING":
                                production.start()
                            if status == "PAUSED":
                                production.pause()
                            productionOrders[po["id"]] = productionOrders
                            


                        colony = Colony(id, name, orbitSim = orbitSim, locale = surface, ships = ships, vehicles = vehicles, buildings=buildings, productionOrders=productionOrders)
                        self._colonies[id] = colony
                        




    ###TODO: This has been copy/pasted a few times now, should really go in its own utility library with a few other commonly used patterns
    def newColonyId(self):
        nodeIdCounter = 0
        while True:
            yield nodeIdCounter
            nodeIdCounter += 1
    
    def createColony(self, name="Default Colony"):
        id = next(self.idGenerator)
        colony = Colony(id, name)
        self._colonies[id] = colony
        return id
    
    def colonyById(self, id):
        return getIntId(id, self._colonies)
    
    def reactionById(self, id):
        return getStringId(id, self._reactions)
    
    def buildingClassById(self, id):
        return getStringId(id, self._buildingClasses)


        