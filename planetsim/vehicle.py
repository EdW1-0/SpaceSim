from utility.vessel import Vessel


class Vehicle(Vessel):
    def __init__(self, id, name, vehicleClass, fuel=0, cargo=None):
        super().__init__(cargo)
        self.id = id
        self.name = name
        self.vehicleClass = vehicleClass
        self.fuel = fuel

    def maxV(self):
        return self.vehicleClass.maxV

    def fuelPerM(self):
        return self.vehicleClass.fuelPerM
