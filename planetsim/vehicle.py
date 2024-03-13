from utility.vessel import Vessel
 
import enum

class VehicleStatus(enum.StrEnum):
    CONSTRUCTION = "CONSTRUCTION"
    IDLE = "IDLE"
    ACTIVE = "ACTIVE"

class VehicleStatusError(Exception):
    pass

class Vehicle(Vessel):
    def __init__(self, id, name, vehicleClass, fuel=0, cargo=None, status=VehicleStatus.CONSTRUCTION, constructionProgress=0):
        super().__init__(cargo)
        self.id = id
        self.name = name
        self.vehicleClass = vehicleClass
        self.fuel = fuel
        self.status = status
        if self.status == VehicleStatus.CONSTRUCTION:
            self.constructionProgress = constructionProgress
        else:
            self.constructionProgress = 100

        self.crew = set()

    def maxV(self):
        return self.vehicleClass.maxV

    def fuelPerM(self):
        return self.vehicleClass.fuelPerM


    def construct(self):
        if self.status != VehicleStatus.CONSTRUCTION:
            raise VehicleStatusError
        self.status = VehicleStatus.IDLE

    def active(self):
        if self.status != VehicleStatus.IDLE:
            raise VehicleStatusError
        self.status = VehicleStatus.ACTIVE

    def idle(self):
        if self.status != VehicleStatus.ACTIVE:
            raise VehicleStatusError
        self.status = VehicleStatus.IDLE