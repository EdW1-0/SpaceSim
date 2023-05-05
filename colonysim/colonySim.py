import os
import json

from colonysim.resource import Resource
from colonysim.reaction import Reaction
from colonysim.buildingClass import BuildingClass

class ColonySim:
    def __init__(self, resourcePath = "json/resources", reactionPath = "json/reactions", buildingPath = "json/buildingClasses"):
        self._buildingClasses = {}
        self._resources = {}
        self._reactions = {}
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


        