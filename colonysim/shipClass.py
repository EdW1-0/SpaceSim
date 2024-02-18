from playerState import PlayerState

class ShipClass:
    def __init__(self, id, name, 
        playerState: PlayerState = None, maxDeltaV=0, constructionTime = 1, constructionCost = {}):
        self.id = id
        self.name = name
        self.maxDeltaV = maxDeltaV
        
        self.playerState = playerState

        self.baseConstructionCost = constructionCost
        self.baseConstructionTime = constructionTime

    def constructionCost(self):
        return self.baseConstructionCost
    
    def constructionTime(self):
        return self.playerState(self.baseConstructionTime) 


