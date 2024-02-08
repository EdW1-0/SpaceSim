class ShipClass:
    def __init__(self, id, name, maxDeltaV=0, constructionTime = 1, constructionCost = {}):
        self.id = id
        self.name = name
        self.maxDeltaV = maxDeltaV

        self.baseConstructionCost = constructionCost
        self.baseConstructionTime = constructionTime

    def constructionCost(self):
        return self.baseConstructionCost
    
    def constructionTime(self):
        return self.baseConstructionTime


