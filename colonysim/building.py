import enum

class BuildingStatus(enum.Enum):
    CONSTRUCTION = 0
    IDLE = 1
    ACTIVE = 2

class Building:
    def __init__(self, id, buildingClass):
        self.id = id
        self.buildingClass = buildingClass
        self.status = BuildingStatus.CONSTRUCTION
        self.condition = 100.0
