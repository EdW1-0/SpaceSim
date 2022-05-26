class TechNode:
    def __init__(self, id, name = "", description = "", cost = 0, ancestors = [], effects = []):
        self.id = id
        self.name = name
        self.description = description
        self.cost = cost
        self.ancestors = ancestors
        self.effects = effects