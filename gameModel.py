from techtree.techTree import TechTree
from orbitsim.orbitSim import OrbitSim
from planetsim.planetSim import PlanetSim
from timingMaster import TimingMaster

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
        self.timingMaster = None
        self.init = False

    def load(self, jsonRoot = "json", reload = False):

        if not reload and self.init:
            print ("Already loaded")
            return
        
        # TODO: Wrap these in a try/catch to do special exception handling rather than just the default file errors.
        self.techTree = TechTree(jsonRoot + "/Technologies.json")
        self.orbitSim = OrbitSim(jsonRoot + "/Orbits.json", jsonRoot + "/Particles.json")
        self.planetSim = PlanetSim(jsonRoot + "/Planets.json", vehicleClassPath="json/vehicleClasses")
        
        self.orbitSim.validatePlanets(self.planetSim)

        self.timingMaster = TimingMaster(0)
        # If we got here all the module loads succeeded so set our init flag
        self.init = True

    def get_init(self):
        return self.init
    
    def tick(self):
        if not self.timingMaster:
            return
        
        start = self.timingMaster.timestamp
        self.timingMaster.tick()
        end = self.timingMaster.timestamp
        
        increment = end - start
        if increment:
            self.techTree.tick(increment)
            self.orbitSim.tick(increment)
            self.planetSim.tick(increment)
    
