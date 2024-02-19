import json

class PlayerState:
    def __init__(self, filePath = "json/Parameters.json"):
        self._parameters = {}

        file = open(filePath, "r")

        jsonData = json.load(file)

        for param in jsonData["Parameters"]:
            self._parameters[param] = [1.0]

        file.close()

    def _paramSum(self, paramId):
        return sum(self._parameters[paramId])

    def constructionTime(self, environId: str, base: int):
        general = self._paramSum("GENERAL_CONSTRUCTION_SPEED")
        if environId == "MARTIAN":
            environ = self._paramSum("MARTIAN_CONSTRUCTION_SPEED")
        elif environId == "ORBITAL":
            environ = self._paramSum("ORBITAL_CONSTRUCTION_SPEED")
        elif environId == "AEROSTAT":
            environ = self._paramSum("AEROSTAT_CONSTRUCTION_SPEED")
        elif environId == "PLUTONIC":
            environ = self._paramSum("PLUTONIC_CONSTRUCTION_SPEED")
        else:
            environ = 1.0

        return base / general / environ 
    
    def constructionCost(self, environId: str, base: dict):
        general = self._paramSum("GENERAL_CONSTRUCTION_COST_MODIFIER")

        if environId == "MARTIAN":
            environ = self._paramSum("MARTIAN_CONSTRUCTION_COST_MODIFIER")
        elif environId == "ORBITAL":
            environ = self._paramSum("ORBITAL_CONSTRUCTION_COST_MODIFIER")
        elif environId == "AEROSTAT":
            environ = self._paramSum("AEROSTAT_CONSTRUCTION_COST_MODIFIER")
        elif environId == "PLUTONIC":
            environ = self._paramSum("PLUTONIC_CONSTRUCTION_COST_MODIFIER")
        else:
            environ = 1.0

        return {key: base[key] / general / environ for key in base}
    
    def shipConstructionTime(self, base: int):
        modifier = self._paramSum("SHIP_CONSTRUCTION_TIME_MODIFIER")
        return base / modifier
    
    def applyModifier(self, id, modifier):
        if id not in self._parameters:
            raise KeyError
        self._parameters[id].append(modifier)

# Things to figure out:
    # How this class gets modifiers it needs (from playerTech or elsewhere)
    # I think possibly they should be stored here. PlayerTech then acts on these.
    # How they get stored. Do they go here at all? Should this class be merged with playerTech?
    # How modifiers get matched up with with ids 
    # ID for class should have all relevant metadata
    # i.e. how do we know that lunar chemical plant needs general construction, lunar construction and chemical engineering tech modifiers applying
    # plus presumably secondary ones from staff efficiency, experience etc. Where do these come in?
