class BuildingClass:
    def __init__(
        self,
        id,
        name,
        constructionTime=10,
        constructionCost={},
        demolitionTime=5,
        demolitionCost={},
    ):
        self.id = id
        self.name = name
        self.constructionCost = constructionCost
        self.constructionTime = constructionTime
        self.demolitionCost = demolitionCost
        self.demolitionTime = demolitionTime


class ProductionBuildingClass(BuildingClass):
    def __init__(self, *args, reactions={}, **kwargs):
        super(ProductionBuildingClass, self).__init__(*args, **kwargs)
        self.reactions = reactions


class StorageBuildingClass(BuildingClass):
    def __init__(self, *args, stores={}, **kwargs):
        super(StorageBuildingClass, self).__init__(*args, **kwargs)
        self.stores = stores


class ExtractionBuildingClass(BuildingClass):
    def __init__(self, *args, extracts={}, **kwargs):
        super(ExtractionBuildingClass, self).__init__(*args, **kwargs)
        self.extracts = extracts
