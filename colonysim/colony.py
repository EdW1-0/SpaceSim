class Colony:
    def __init__(self, id, name, ships = {}, vehicles = {}):
        self.id = id
        self.name = name
        self.ships = ships
        self.vehicles = vehicles
        self.buildings = {}