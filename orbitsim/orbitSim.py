import json

from orbitsim.orbitNode import OrbitNode

class OrbitSim:
    def __init__(self, jsonPath = "json/Orbits.json"):
        jsonFile = open(jsonPath, "r")

        jsonBlob = json.load(jsonFile)

        orbitalsArray = jsonBlob["Orbitals"]

        def stripLinks(x):
            if "links" in x:
                del x["links"]
            return x
        orbitalsDelinked = map(stripLinks, orbitalsArray)
        self._nodes = {node["id"]: OrbitNode(**node) for node in orbitalsDelinked}
        
        self._particles = []
        self._links = []

    def nodeById(self, id):
        if not isinstance(id, int):
            raise TypeError
        elif id < 0:
            raise ValueError
        return self._nodes[id]