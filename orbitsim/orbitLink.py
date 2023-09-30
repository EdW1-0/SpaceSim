from orbitsim.orbitNode import OrbitNode


class OrbitLink:
    def __init__(self, id, topNode, bottomNode, deltaV=0, travelTime=0, distance=0):
        self.particles = {}
        self.id = id
        self.topNode = topNode
        self.bottomNode = bottomNode
        if self.topNode == self.bottomNode:
            raise TypeError
        self.deltaV = deltaV
        self.travelTime = travelTime
        self.distance = distance
