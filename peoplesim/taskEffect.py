from dataclasses import dataclass

from colonysim import BuildingStatus

@dataclass(frozen=True)
class TaskEffect:
    pass

@dataclass(frozen=True)
class TaskEffectStateChange(TaskEffect):
    state: str
    value: BuildingStatus

    def __str__(self):
        return "Change {0}: {1}".format(self.state, self.value)
    
@dataclass(frozen=True)
class TaskEffectParameter(TaskEffect):
    parameter: str
    amount: int

    def __str__(self):
        return "Modify {0}: {1}".format(self.parameter, self.amount)

