class OrbitNode:
    def __init__(self, id, name = "", planet = None, gravity = 0):
        self.links = []
        self.particles = []

        self.id = id
        self.name = name
        self.gravity = gravity
        self.planet = planet
