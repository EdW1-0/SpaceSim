from dataclasses import dataclass
from enum import Enum

class TechEffectClass(Enum):
    BUILDING = 0
    VEHICLE = 1

@dataclass(frozen=True)
class TechEffect:
    effect: TechEffectClass
    value: int

class TechNode:
    def __init__(self, id, name = "", description = "", cost = 0, ancestors = [], effects = []):
        self.id = id
        self.name = name
        self.description = description
        self.cost = cost
        self.ancestors = ancestors
        self.effects = [TechEffect(TechEffectClass[e["effect"]], e["value"]) for e in effects]

