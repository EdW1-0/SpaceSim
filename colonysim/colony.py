from colonysim.building import Building, ProductionBuilding, StorageBuilding, BuildingStatus, ExtractionBuilding
from colonysim.buildingClass import BuildingClass, ProductionBuildingClass, StorageBuildingClass, ExtractionBuildingClass
from colonysim.productionOrder import ProductionOrder, OrderStatus
from planetsim.planetSurface import PlanetSurface
from planetsim.vehicle import Vehicle

class Colony:
    def __init__(self, id, name, orbitSim = None, locale = None, ships = [], vehicles = [], buildings = None):
        self.id = id
        self.name = name
        self.orbitSim = orbitSim
        self.locale = locale
        if buildings:
            self.buildings = buildings
        else:
            self.buildings = {}
        self.buildingIdGenerator = self.newBuildingId()
        self.productionOrders = {}
        self.productionOrderIdGenerator = self.newProductionOrderId()
        self.ships = {}
        for shipId in ships:
            ship = orbitSim.transferShip(shipId)
            self.ships[shipId] = ship

        self.vehicles = {}
        for vehicleId in vehicles:
            vehicle = locale.transferVehicle(vehicleId)
            self.vehicles[vehicleId] = vehicle

        if locale:
            self.locale.connectColony(id)

        # Things to do here:
        # - Get ships from orbitSim
        # - Get vehicles from locale
        # - Create buildings
        # - Link colony up on locale


    def newBuildingId(self):
        buildingIdCounter = 0
        while True:
            while buildingIdCounter in self.buildings:
                buildingIdCounter += 1
            yield buildingIdCounter

    def newProductionOrderId(self):
        productionIdCounter = 0
        while True:
            while productionIdCounter in self.productionOrders:
                productionIdCounter += 1
            yield productionIdCounter


    # Question over whether this should be given a buildingClass reference directly, or just an id and look it up from colonySim.
    # I think this should be OK even though we will proliferate refs to buildingClass instances - these should all be singleton objects
    # with lifespan equal to the life of the game instance anyway, and this saves an extra lookup through colonysim. 
    def addBuilding(self, buildingClass, colonySim = None):
        id = next(self.buildingIdGenerator)
        if isinstance(buildingClass, ProductionBuildingClass):
            self.buildings[id] = ProductionBuilding(id, buildingClass, colonySim)
        elif isinstance(buildingClass, StorageBuildingClass):
            self.buildings[id] = StorageBuilding(id, buildingClass)
        elif isinstance(buildingClass, ExtractionBuildingClass):
            self.buildings[id] = ExtractionBuilding(id, buildingClass)
        elif isinstance(buildingClass, BuildingClass):
            self.buildings[id] = Building(id, buildingClass)
        else:
            raise TypeError
        return id
    
    def productionBuildings(self):
        return [building for building in self.buildings.values() if isinstance(building, ProductionBuilding)]
    
    def extractionBuildings(self):
        return [building for building in self.buildings.values() if isinstance(building, ExtractionBuilding)]

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
    
    def demolishBuilding(self, id):
        building = self.buildingById(id)
        return building.demolish()
    
    def removeBuilding(self, id):
        del self.buildings[id]
    
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
    
    def addShip(self, name, shipClass, deltaV = 0):
        shipId = self.orbitSim.createShip(name, shipClass, deltaV)
        ship = self.orbitSim.transferShip(shipId)
        self.ships[shipId] = ship

    def addVehicle(self, name, fuel = 0):
        if not self.locale and not isinstance(self.locale, PlanetSurface):
            raise TypeError
        vehicleId = self.orbitSim.getVehicleId()
        vc = next(iter(self.locale.vehicleClasses.values()))
        vehicle = Vehicle(vehicleId, name, vc, fuel)
        self.vehicles[vehicleId] = vehicle
        return vehicleId
    
    def tick(self, increment):
        while increment:
            increment -= 1
            self.tickExtraction()
            self.tickProduction()
            self.tickConstruction()
            self.tickDemolition()


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
    def tickProduction(self):
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

    def tickExtraction(self):
        for building in self.extractionBuildings():
            if building.status == BuildingStatus.ACTIVE:
                production = building.extract()
                wastage = self.storeResources(building.material(), production)

    def tickConstruction(self):
        for building in self.buildings.values():
            if building.status == BuildingStatus.CONSTRUCTION:
                if building.constructionProgress == building.buildingClass.constructionTime:
                    self.constructBuilding(building.id)
                else:
                    building.constructionProgress += 1

    def tickDemolition(self):
        removeIds = []
        for building in self.buildings.values():
            if building.status == BuildingStatus.DEMOLITION:
                if building.demolitionProgress == building.buildingClass.demolitionTime:
                    removeIds.append(building.id)
                else:
                    building.demolitionProgress += 1

        for id in removeIds:
            self.removeBuilding(id)
                

    
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
