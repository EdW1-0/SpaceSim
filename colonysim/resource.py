class Resource:
    def __init__(self, id, name, baseValue = 1.0, units = "kg"):
        self.id = id
        self.name = name
        self.baseValue = baseValue
        self.units = units