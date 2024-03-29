from techtree.techEffect import TechEffectUnlock, TechEffectParameter
from techtree.techTree import TechTree
from techtree.techNode import TechNode

# TODO: Not sure it should be resposibility of this class to be passed tech tree.
# Think it should just discover instance internally.
class PlayerTech:
    def __init__(self, techTree: TechTree=None):
        self._discovered = {
            "TECH": set(),
            "BUILDING": set(),
            "VEHICLE": set(),
            "SHIP": set()
        }
        self.techTree: TechTree = techTree
        self.activeTech: TechNode = None
        self.progress: int = 0

        self.parameterModifierCallback = None

    def setActiveTech(self, id: str):
        if id not in self.possibleTargets:
            return 
        
        tech = self.techTree.nodeById(id)
        self.activeTech = tech
        self.progress = 0

    def _completeTech(self):
        if self.activeTech:
            self._discovered["TECH"].add(self.activeTech.id)
            self._processEffects(self.activeTech.effects)
            self.activeTech = None
        else:
            raise ValueError

    def _processEffects(self, effects):
        for effect in effects:
            if isinstance(effect, TechEffectUnlock):
                self._discovered[effect.domain].add(effect.id)
            elif isinstance(effect, TechEffectParameter):
                self.parameterModifierCallback(effect.parameter, effect.amount)


    def addResearch(self, increment: int):
        self.progress += increment
        if self.activeTech and self.progress >= self.activeTech.cost:
            self._completeTech()
            self.progress = 0

    def tick(self, increment: int):
        if self.activeTech:
            self.addResearch(1)

    @property
    def discoveredTechs(self):
        return self._discovered["TECH"]
    
    @property
    def discoveredBuildings(self):
        return self._discovered["BUILDING"]
    
    @property
    def discoveredShips(self):
        return self._discovered["SHIP"]
    
    @property
    def discoveredVehicles(self):
        return self._discovered["VEHICLE"]
    
    def parameter(self, param):
        return sum(self._discovered[param])

    @property
    def possibleTargets(self):
        targets = set()
        # For each tech in tree
        for id in self.techTree.nodes.keys():
            # If discovered, reject
            if id not in self._discovered["TECH"]:
                # Else for each tech in ancestors
                ancestorsDiscovered = True
                for ancestor in self.techTree.nodeById(id).ancestors:
                    # If not in discovered, reject
                    if ancestor not in self._discovered["TECH"]:
                        ancestorsDiscovered = False

                if ancestorsDiscovered:
                    targets.add(id)

        return targets
