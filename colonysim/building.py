import enum

class BuildingStatus(enum.Enum):
    CONSTRUCTION = 0
    IDLE = 1
    ACTIVE = 2

class BuildingStatusError(Exception):
    pass

class Building:
    def __init__(self, id, buildingClass):
        self.id = id
        self.buildingClass = buildingClass
        self.status = BuildingStatus.CONSTRUCTION
        self.condition = 100.0

    def construct(self):
        if self.status != BuildingStatus.CONSTRUCTION:
            raise BuildingStatusError
        self.status = BuildingStatus.IDLE
        
    def start(self):
        if self.status != BuildingStatus.IDLE:
            raise BuildingStatusError
        self.status = BuildingStatus.ACTIVE
        
    def stop(self):
        if self.status != BuildingStatus.ACTIVE:
            raise BuildingStatusError
        self.status = BuildingStatus.IDLE

class ProductionBuilding(Building):
    def __init__(self, id, buildingClass, colonySim):
        super(ProductionBuilding, self).__init__(id, buildingClass)
        self.reaction = next(iter(buildingClass.reactions))
        self.rate = self.buildingClass.reactions[self.reaction]
        self.colonySim = colonySim

    def setReaction(self, id):
        self.reaction = id
        self.rate = self.buildingClass.reactions[self.reaction]

    def react(self, reactants, quota = None):
        # Algorithm for this:
        # Sanity checking on reactants type etc.
        # Check reactants has each of required inputs.
        # Then formula is - each of reactants in proportions from reaction * efficiency of building
        # If all inputs have enough, then this is the reaction that happens.
        # If one or more is short, find ratio of available input to max input
        # Find smallest ratio
        # Multiply all reactants by this ratio
        # Compute output dict - subtract inputs from starting reactants and add outputs.
        # Algorithm should ignore any unused reactants and pass them through unchanged
        # Algorithm should not care if outputs are not in reactant dict, but should add them to output dict
        if not isinstance(reactants, dict):
            raise TypeError

        reaction = self.colonySim.reactionById(self.reaction)
        for input in reaction.inputs:
            if input not in reactants:
                raise KeyError
            
        if quota is None:
            quota = 99999999
            
        inputs = reaction.inputs.copy()
        outputs = reaction.outputs.copy()
        endstate = reactants.copy()
        minFraction = 1.0
        for i in inputs:
            inputs[i] *= min(self.rate, quota)
            if inputs[i] > endstate[i]:
                minFraction = min(minFraction, endstate[i]/inputs[i])

        for i in inputs:
            endstate[i] -= inputs[i] * minFraction

        for o in outputs:
            outputs[o] *= min(quota, self.rate) * minFraction
            if o in endstate:
                endstate[o] += outputs[o]
            else:
                endstate[o] = outputs[o]

        return endstate




class StorageBuilding(Building):
    def __init__(self, id, buildingClass):
        super(StorageBuilding, self).__init__(id, buildingClass)
        self.amount = 0
        self.contents = next(iter(buildingClass.stores))
        
    def setContents(self, id):
        self.buildingClass.stores[id]
        if self.amount > 0:
            raise ValueError
        self.contents = id

    def capacity(self):
        return self.buildingClass.stores[self.contents]
    
    def add(self, amount):
        if not (isinstance(amount, dict)):
            raise TypeError
        elif not (len(amount) == 1):
            raise ValueError
        
        value = amount[self.contents]
        if value <= (self.capacity() - self.amount):
            self.amount += value
            excess = 0
        else:
            excess = value - (self.capacity() - self.amount)
            self.amount = self.capacity()

        return excess      
    
    def remove(self, amount):
        if not (isinstance(amount, dict)):
            raise TypeError
        elif not (len(amount) == 1):
            raise ValueError
        
        value = amount[self.contents]
        supply = min(value, self.amount)
        self.amount -= supply

        return supply

        



