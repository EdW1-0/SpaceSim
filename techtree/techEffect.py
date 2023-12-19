from dataclasses import dataclass

@dataclass(frozen=True)
class TechEffect:
    pass

@dataclass(frozen=True)
class TechEffectUnlock(TechEffect):
    domain: str
    id: str 

    def __str__(self):
        return "Unlock {0} {1}".format(self.domain, self.id)

@dataclass(frozen=True)
class TechEffectParameter(TechEffect):
    parameter: str
    amount: int

    def __str__(self):
        return "Modify {0}: {1}".format(self.parameter, self.amount)
