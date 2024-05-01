class TaskClass:
    def __init__(self, id: str, name: str = "", inputs: list = None, duration: int = 1, effects: list = None):
        self.id = id
        self.name = name
        self.inputs = inputs
        self.duration = duration
        self.effects =  effects