class VehicleClass:
    def __init__(self, id, name, maxFuel=0, maxV=0, fuelPerM=0, constructionTime=1, constructionCost = {}):
        self.id = id
        self.name = name
        self.maxFuel = maxFuel
        self.maxV = maxV
        self.fuelPerM = fuelPerM

        self.baseConstructionCost = constructionCost
        self.baseConstructionTime = constructionTime

    def constructionCost(self):
        return self.baseConstructionCost
    
    def constructionTime(self):
        return self.baseConstructionTime