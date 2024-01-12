import json

class PlayerState:
    def __init__(self, filePath = "json/Parameters.json"):
        self._parameters = {}

        file = open(filePath, "r")

        jsonData = json.load(file)

        for param in jsonData["Parameters"]:
            self._parameters[param] = [1.0]

        file.close()

    def constructionTime(self, id, base):
        return base
    
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
