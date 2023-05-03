class Reaction:
    def __init__(self, id, name, inputs = {}, products = {}):
        self.id = id
        self.name = name
        self.inputs = inputs
        self.products = products