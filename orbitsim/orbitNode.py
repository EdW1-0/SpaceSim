class OrbitNode:
    def __init__(self, planet = None, gravity = 0):
        self.links = []
        self.particles = []
        self.gravity = gravity
        self.planet = planet
