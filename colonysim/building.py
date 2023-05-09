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
    def __init__(self, *args, **kwargs):
        super(ProductionBuilding, self).__init__(*args, **kwargs)

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

        



