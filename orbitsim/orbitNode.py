from enum import Enum

class LeafClass(Enum):
    NONE = 0
    ROOT = 1
    PLANET = 2
    MOON = 3

class OrbitNode:
    def __init__(self, id, name = "", planet = None, gravity = 0, leaf = LeafClass.NONE):
        self.links = []
        self.particles = set()

        self.id = id
        self.name = name
        self.planet = planet
        self.leaf = LeafClass(leaf)
