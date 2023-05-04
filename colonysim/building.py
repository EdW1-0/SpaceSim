class Building:
    def __init__(self, id, buildingClass):
        self.id = id
        self.buildingClass = buildingClass
        self.active = False
        self.condition = 100.0