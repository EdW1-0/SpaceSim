from colonysim.building import Building, ProductionBuilding, StorageBuilding, BuildingStatus
from colonysim.buildingClass import BuildingClass, ProductionBuildingClass, StorageBuildingClass
from colonysim.productionOrder import ProductionOrder, OrderStatus

class Colony:
    def __init__(self, id, name, ships = {}, vehicles = {}):
        self.id = id
        self.name = name
        self.ships = ships
        self.vehicles = vehicles
        self.buildings = {}
        self.buildingIdGenerator = self.newBuildingId()
        self.productionOrders = {}
        self.productionOrderIdGenerator = self.newProductionOrderId()

    def newBuildingId(self):
        buildingIdCounter = 0
        while True:
            yield buildingIdCounter
            buildingIdCounter += 1

    def newProductionOrderId(self):
        productionIdCounter = 0
        while True:
            yield productionIdCounter
            productionIdCounter += 1


    # Question over whether this should be given a buildingClass reference directly, or just an id and look it up from colonySim.
    # I think this should be OK even though we will proliferate refs to buildingClass instances - these should all be singleton objects
    # with lifespan equal to the life of the game instance anyway, and this saves an extra lookup through colonysim. 
    def addBuilding(self, buildingClass, colonySim = None):
        id = next(self.buildingIdGenerator)
        if isinstance(buildingClass, ProductionBuildingClass):
            self.buildings[id] = ProductionBuilding(id, buildingClass, colonySim)
        elif isinstance(buildingClass, StorageBuildingClass):
            self.buildings[id] = StorageBuilding(id, buildingClass)
        elif isinstance(buildingClass, BuildingClass):
            self.buildings[id] = Building(id, buildingClass)
        else:
            raise TypeError
        return id
    
    def productionBuildings(self):
        return [building for building in self.buildings.values() if isinstance(building, ProductionBuilding)]

    def addProductionOrder(self, reaction, amount):
        id = next(self.productionOrderIdGenerator)
        self.productionOrders[id] = ProductionOrder(id, reaction, amount)
        return id
    
    def constructBuilding(self, id):
        building = self.buildingById(id)
        return building.construct()
    
    def activateBuilding(self, id):
        building = self.buildingById(id)
        return building.start()
    
    def idleBuilding(self, id):
        building = self.buildingById(id)
        return building.stop()
    
    def startProductionOrder(self, id):
        order = self.productionOrderById(id)
        return order.start()
    
    def pauseProductionOrder(self, id):
        order = self.productionOrderById(id)
        return order.pause()
    
    # Try to get the full amount requested by removing it from each of our stores, but if can't fully satisfy, send all that we do have.
    def getResources(self, resource, quantity):
        requisitioned = 0
        for b in self.buildings.values():
            if isinstance(b, StorageBuilding) and b.contents == resource:
                requisitioned += b.remove({resource: quantity - requisitioned})
                if requisitioned == quantity:
                    break

        return requisitioned

    def storeResources(self, resource, quantity):
        surplus = quantity
        for b in self.buildings.values():
            if isinstance(b, StorageBuilding) and b.contents == resource:
                surplus = b.add({resource: surplus})
                if surplus == 0:
                    break
        return surplus

    
    def tick(self, increment):
        while increment:
            increment -= 1
            for po in self.productionOrders.values():
                if not po.status == OrderStatus.RUNNING:
                    continue

                inputs = po.reaction.inputs.copy()
                workingDict = {}
                for i in inputs:
                    # May not be the full amount, depending on what we have in stores. That's OK, work with what we have. mrd
                    workingDict[i] = self.getResources(i, inputs[i]*po.amount)

                for pb in self.productionBuildings():
                    if pb.status == BuildingStatus.ACTIVE and pb.reaction == po.reaction.id:
                        # Run reaction, and measure how much actually got done.
                        prior = next(iter(workingDict.values()))
                        workingDict = pb.react(workingDict, po.remaining)
                        post = next(iter(workingDict.values()))
                        # Should be 1.0 if enough resources for reaction
                        # Should just pass this as return val from react
                        ratio = (prior - post)/next(iter(inputs.values()))
                        po.remaining -= ratio
                    if po.remaining <= 0:
                        break

                for r in workingDict:
                    # Not all products can necessarily be stored so record how much is wasted.
                    wastage = self.storeResources(r, workingDict[r])





            # Algorithm for this:
            # Get input reagants and amounts
            # Request them from stores - needs own method
            # Do we bother with fractionals or just bust if not enough?
            # Then look for available production buildings - may abstract into own method
            # On each pb,
            #   Call react with product set
            #   Decrement remaining
            # Once remaining = 0 or no more pbs, 
            # return product set to stockpile - needs own method

    
    def buildingById(self, id):
        if not isinstance(id, int):
            raise TypeError
        elif id < 0:
            raise ValueError
        return self.buildings[id]

    def productionOrderById(self, id):
        if not isinstance(id, int):
            raise TypeError
        elif id < 0:
            raise ValueError
        return self.productionOrders[id]
