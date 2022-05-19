import os
import json


import techNode


class TechTree:
    def __init__(self, jsonPath = "json/Technologies.json"):
        jsonFile = open(jsonPath, "r")
        jsonTechs = json.load(jsonFile)

        jsonNodes = jsonTechs["Technologies"]
        self.nodes = [techNode.TechNode(**node) for node in jsonNodes]
        self.totalNodes = len(self.nodes)

    def nodeById(self, id):
        if not isinstance(id, int):
            raise TypeError
        elif id < 0:
            raise ValueError
        return self.nodes[id]
