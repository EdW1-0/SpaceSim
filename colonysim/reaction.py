class Reaction:
    def __init__(self, id, name, inputs = {}, outputs = {}):
        self.id = id
        self.name = name
        self.inputs = inputs
        self.outputs = outputs