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
        self.gravity = gravity ###TODO: I think this attribute is redundant, only Planet needs to know this. Confirm this and delete if so.
        self.planet = planet
        self.leaf = LeafClass(leaf)
