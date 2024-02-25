import os
import json

from colonysim.resource import Resource
from colonysim.reaction import Reaction
from colonysim.buildingClass import (
    BuildingClass,
    ProductionBuildingClass,
    StorageBuildingClass,
    ExtractionBuildingClass,
    ResearchBuildingClass
)
from colonysim.building import (
    Building,
    ProductionBuilding,
    StorageBuilding,
    ExtractionBuilding,
)
from colonysim.colony import Colony
from colonysim.productionOrder import ProductionOrder

from utility import loadEntityFile, getIntId, getStringId, IDGenerator

from techtree import PlayerTech
from playerState import PlayerState


class ColonySim:
    def __init__(
        self,
        orbitSim=None,
        planetSim=None,
        playerTech: PlayerTech=None,
        playerState: PlayerState=None,
        colonyPath="json/colonies",
        resourcePath="json/resources",
        reactionPath="json/reactions",
        buildingPath="json/buildingClasses",
    ):
        self.orbitSim = orbitSim
        self.planetSim = planetSim
        self.playerTech = playerTech
        if self.playerTech:
            ptCallback = self.playerTech.addResearch
        else:
            ptCallback = None
        self.playerState = playerState
        self._buildingClasses = {}
        self._resources = {}
        self._reactions = {}

        self.idGenerator = IDGenerator()
        self._colonies = {}

        self._resources = loadEntityFile(resourcePath, "Resources", Resource)

        self._reactions = loadEntityFile(reactionPath, "Reactions", Reaction)

        self._buildingClasses = loadEntityFile(
            buildingPath,
            "Buildings",
            BuildingClass,
            {
                "reactions": ProductionBuildingClass,
                "stores": StorageBuildingClass,
                "extracts": ExtractionBuildingClass,
                "researchOutput": (ResearchBuildingClass, {"researchCallback": ptCallback}),
            },
            playerState = self.playerState,
        )

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
                                building.constructionProgress = b[
                                    "constructionProgress"
                                ]
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
                            productionOrders[po["id"]] = production

                        colony = Colony(
                            id,
                            name,
                            orbitSim=orbitSim,
                            locale=surface,
                            ships=ships,
                            vehicles=vehicles,
                            buildings=buildings,
                            productionOrders=productionOrders,
                        )
                        self._colonies[id] = colony
                        self.idGenerator.setId(id)


    def createColony(self, name="Default Colony", locale=None):
        id = self.idGenerator.generateId()
        colony = Colony(id, name, orbitSim=self.orbitSim, locale=locale)
        self._colonies[id] = colony
        return colony

    def tick(self, increment):
        for colony in self._colonies.values():
            colony.tick(increment)

    def colonyForShipId(self, shipId):
        for colony in self._colonies.values():
            if shipId in colony.ships:
                return colony

        return None

    def buildingClassesForColony(self, colonyId):
        return {key: self._buildingClasses[key] for key in self._buildingClasses if key in self.playerTech.discoveredBuildings}
    
    def shipClassesForColony(self, colonyId):
        return {key: self.orbitSim._shipClasses[key] for key in self.orbitSim._shipClasses if key in self.playerTech.discoveredShips}

    def vehicleClassesForColony(self, colonyId):
        return {key: self.planetSim.vehicleClasses[key] for key in self.planetSim.vehicleClasses if key in self.playerTech.discoveredVehicles}

    def colonyById(self, id):
        return getIntId(id, self._colonies)

    def resourceById(self, id):
        return getStringId(id, self._resources)

    def reactionById(self, id):
        return getStringId(id, self._reactions)

    def buildingClassById(self, id):
        return getStringId(id, self._buildingClasses)
