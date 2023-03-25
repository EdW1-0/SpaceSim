import json

from planetsim.planet import Planet

class PlanetSim:
    def __init__(self, jsonPath = "json/Planets.json"):
        jsonFile = open(jsonPath, "r")
        jsonPlanets = json.load(jsonFile)

        jsonNodes = jsonPlanets["Planets"]

        self.planets = {node["id"]: Planet(**node) for node in jsonNodes}

    def planetById(self, id):
        if not isinstance(id, int):
            raise TypeError
        elif id < 0:
            raise ValueError
        return self.planets[id]
