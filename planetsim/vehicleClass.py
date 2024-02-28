from playerState import PlayerState

class VehicleClass:
    def __init__(self, 
                 id: str, 
                 name: str, 
                 playerState: PlayerState = None, 
                 maxFuel: int=0, 
                 maxV: int=0, 
                 fuelPerM: float=0, 
                 constructionTime: int=1, 
                 constructionCost: dict = {}) -> None:
        self.id = id
        self.name = name
        self.maxFuel = maxFuel
        self.maxV = maxV
        self.fuelPerM = fuelPerM
        self.playerState = playerState

        self.baseConstructionCost = constructionCost
        self.baseConstructionTime = constructionTime

    def constructionCost(self) -> dict:
        return self.baseConstructionCost
    
    def constructionTime(self) -> int:
        return self.playerState.vehicleConstructionTime(self.baseConstructionTime)
