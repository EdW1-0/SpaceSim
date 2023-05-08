import os
import json

from colonysim.resource import Resource
from colonysim.reaction import Reaction
from colonysim.buildingClass import BuildingClass
from colonysim.colony import Colony

class ColonySim:
    def __init__(self, resourcePath = "json/resources", reactionPath = "json/reactions", buildingPath = "json/buildingClasses"):
        self._buildingClasses = {}
        self._resources = {}
        self._reactions = {}

        self.idGenerator = self.newBuildingId()
        self._colonies = {}

        self._resources = self.loadEntityFile(resourcePath, "Resources", Resource)

        self._reactions = self.loadEntityFile(reactionPath, "Reactions", Reaction)

        self._buildingClasses = self.loadEntityFile(buildingPath, "Buildings", BuildingClass)

    def loadEntityFile(self, path, id, EntityClass):
        entityDict = {}
        for subdir, dirs, files in os.walk(path):
            for file in files:
                entityFile = open(path + "/" + file, "r")
                entityJson = json.load(entityFile)

                entities = entityJson[id]

                entityDict.update({e["id"]: EntityClass(**e) for e in entities})
                entityFile.close()
        return entityDict
    
    ###TODO: This has been copy/pasted a few times now, should really go in its own utility library with a few other commonly used patterns
    def newBuildingId(self):
        nodeIdCounter = 0
        while True:
            yield nodeIdCounter
            nodeIdCounter += 1
    
    def createColony(self, name="Default Colony"):
        id = next(self.idGenerator)
        colony = Colony(id, name)
        self._colonies[id] = colony
        return id


        