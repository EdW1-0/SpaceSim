from dataclasses import dataclass
from enum import Enum


class TechEffectClass(Enum):
    BUILDING = 0
    VEHICLE = 1


@dataclass(frozen=True)
class TechEffect:
    effect: TechEffectClass
    value: int

@dataclass(frozen=True)
class TechEffectUnlock(TechEffect):
    domain: str
    id: str 

@dataclass(frozen=True)
class TechEffectParameter(TechEffect):
    parameter: str
    amount: int
