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


