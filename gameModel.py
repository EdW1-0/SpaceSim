from techtree.techTree import TechTree
from orbitsim.orbitSim import OrbitSim

class GameModel:
    # Needs:
    # Set of orbits
    # Planet surfaces
    # Tech tree
    # People 
    def __init__(self):
        self.techTree = TechTree()
        self.orbitSim = OrbitSim()