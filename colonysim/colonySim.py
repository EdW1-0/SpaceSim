import os
import json

from colonysim.resource import Resource
from colonysim.reaction import Reaction
from colonysim.buildingClass import BuildingClass, ProductionBuildingClass, StorageBuildingClass, ExtractionBuildingClass
from colonysim.colony import Colony

from utility.fileLoad import loadEntityFile

class ColonySim:
    def __init__(self, resourcePath = "json/resources", reactionPath = "json/reactions", buildingPath = "json/buildingClasses"):
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


        