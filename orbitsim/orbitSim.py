import json

from orbitsim.orbitNode import OrbitNode

class OrbitSim:
    def __init__(self, jsonPath = "json/Orbits.json"):
        jsonFile = open(jsonPath, "r")

        jsonBlob = json.load(jsonFile)

        orbitalsArray = jsonBlob["Orbitals"]
        self._nodes = {node["id"]: OrbitNode(**node) for node in orbitalsArray}
        self._particles = []
        self._links = []

    def nodeById(self, id):
        if not isinstance(id, int):
            raise TypeError
        elif id < 0:
            raise ValueError
        return self._nodes[id]