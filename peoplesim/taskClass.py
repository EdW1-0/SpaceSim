from peoplesim.taskEffect import TaskEffectStateChange, TaskEffectParameter

class TaskClass:
    def __init__(self, id: str, name: str = "", inputs: list = None, duration: int = 1, effects: list = None):
        self.id = id
        self.name = name
        self.inputs = inputs
        self.duration = duration
        self.effects = []
        for effect in effects:
            if effect["type"] == "STATE":
                self.effects.append(TaskEffectStateChange(
                    state = effect["state"],
                    value = effect["value"]
                ))
            elif effect["type"] == "PARAMETER":
                self.effects.append(TaskEffectParameter(
                    parameter = effect["parameter"],
                    amount = effect["amount"]
                ))
