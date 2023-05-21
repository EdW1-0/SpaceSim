class Vehicle:
    def __init__(self, id, name, vehicleClass, fuel = 0):
        self.id = id
        self.name = name
        self.vehicleClass = vehicleClass
        self.fuel = fuel

    def maxV(self):
        return self.vehicleClass.maxV
    
    def fuelPerM(self):
        return self.vehicleClass.fuelPerM