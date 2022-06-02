from orbitsim.orbitNode import OrbitNode

class OrbitLink:
    def __init__(self, topNode, bottomNode, deltaV = 0, travelTime = 0, distance = 0):
        self.particles = []
        self.topNode = topNode
        self.bottomNode = bottomNode
        if not topNode or not bottomNode:
            raise TypeError
        self.deltaV = deltaV
        self.travelTime = deltaV
        self.distance = deltaV