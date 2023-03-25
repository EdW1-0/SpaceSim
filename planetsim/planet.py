class Planet:
    def __init__(self, id, name, gravity, surface = None, atmosphere = None):
        self.id = id
        self.name = name
        self.surface = surface
        self.atmosphere = atmosphere
        self.gravity = gravity