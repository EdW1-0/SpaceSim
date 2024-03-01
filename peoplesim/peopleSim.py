from utility import loadEntityFile
from peoplesim.person import Person

class PeopleSim:
    def __init__(self, jsonPath: str = "json/people"):
        self._people = loadEntityFile(jsonPath, "People", Person)