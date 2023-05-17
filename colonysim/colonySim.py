import os
import json

from colonysim.resource import Resource
from colonysim.reaction import Reaction
from colonysim.buildingClass import BuildingClass, ProductionBuildingClass, StorageBuildingClass, ExtractionBuildingClass
from colonysim.colony import Colony

class ColonySim:
    def __init__(self, resourcePath = "json/resources", reactionPath = "json/reactions", buildingPath = "json/buildingClasses"):
        self._buildingClasses = {}
        self._resources = {}
        self._reactions = {}

        self.idGenerator = self.newColonyId()
        self._colonies = {}

        self._resources = self.loadEntityFile(resourcePath, "Resources", Resource)

        self._reactions = self.loadEntityFile(reactionPath, "Reactions", Reaction)

        self._buildingClasses = self.loadEntityFile(buildingPath, 
                                                    "Buildings", 
                                                    BuildingClass, 
                                                    {
                                                        "reactions": ProductionBuildingClass,
                                                        "stores": StorageBuildingClass,
                                                        "extracts": ExtractionBuildingClass
                                                        })

    def extractEntityJson(self, path, id):
        entityFile = open(path, "r")
        entityJson = json.load(entityFile)
        entities = entityJson[id]
        entityFile.close()
        return entities

    def loadEntityFile(self, path, id, EntityClass, altClasses = {}):
        entityDict = {}
        for subdir, dirs, files in os.walk(path):
            for file in files:
                entities = self.extractEntityJson(path + "/" + file, id)
                for e in entities:
                    foundAlt = False
                    for altId in altClasses:
                        if altId in e:
                            entityDict.update({e["id"]: altClasses[altId](**e)})
                            foundAlt = True
                            break
                    if not foundAlt:
                        entityDict.update({e["id"]: EntityClass(**e)})
        return entityDict
    
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
    
    def reactionById(self, id):
        if not (type(id) == int or isinstance(id, str)):
            raise TypeError
        elif isinstance(id, str) and not id.isupper():
            raise ValueError 
        return self._reactions[id]


        