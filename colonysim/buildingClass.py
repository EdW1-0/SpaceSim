class BuildingClass:
    def __init__(self, id, name, constructionTime = 10, constructionCost = {}):
        self.id = id
        self.name = name
        self.constructionCost = constructionCost
        self.constructionTime = constructionTime

class ProductionBuildingClass(BuildingClass):
    def __init__(self, *args, reactions = {}, **kwargs):
        super(ProductionBuildingClass, self).__init__(*args, **kwargs)
        self.reactions = reactions