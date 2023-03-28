from techtree.techTree import TechTree
from orbitsim.orbitSim import OrbitSim
from planetsim.planetSim import PlanetSim

class GameModel:
    # Needs:
    # Set of orbits
    # Planet surfaces
    # Tech tree
    # People 
    def __init__(self):
        self.techTree = None
        self.orbitSim = None
        self.planetSim = None
        self.init = False

    def load(self, jsonRoot = "json", reload = False):

        if not reload and self.init:
            print ("Already loaded")
            return
        
        # TODO: Wrap these in a try/catch to do special exception handling rather than just the default file errors.
        self.techTree = TechTree(jsonRoot + "/Technologies.json")
        self.orbitSim = OrbitSim(jsonRoot + "/Orbits.json")
        self.planetSim = PlanetSim(jsonRoot + "/Planets.json")
        # If we got here all the module loads succeeded so set our init flag
        self.init = True

    def get_init(self):
        return self.init
