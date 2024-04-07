from colonysim.building import (
    Building,
    ProductionBuilding,
    StorageBuilding,
    BuildingStatus,
    ExtractionBuilding,
    ResearchBuilding,
)
from colonysim.buildingClass import (
    BuildingClass,
    ProductionBuildingClass,
    StorageBuildingClass,
    ExtractionBuildingClass,
    ResearchBuildingClass,
)
from colonysim.productionOrder import ProductionOrder, OrderStatus
from planetsim.planetSurface import PlanetSurface
from planetsim.vehicle import Vehicle, VehicleStatus
from colonysim.ship import Ship, ShipStatus

from utility import getIntId, IDGenerator

from functools import reduce


class Colony:
    def __init__(
        self,
        id,
        name,
        orbitSim=None,
        locale=None,
        ships=[],
        vehicles=[],
        vehicleFactory=None,
        buildings=None,
        productionOrders=None,
    ):
        self.id = id
        self.name = name
        self.orbitSim = orbitSim
        self.locale = locale
        self.vehicleFactory = vehicleFactory
        if buildings:
            self.buildings = buildings
            for b in self.buildings.values():
                b.locale = self
        else:
            self.buildings = {}
        if productionOrders:
            self.productionOrders = productionOrders
        else:
            self.productionOrders = {}

        self.buildingIdGenerator = IDGenerator()
        self.productionOrderIdGenerator = IDGenerator()
        for building in self.buildings:
            self.buildingIdGenerator.setId(building)
        for po in self.productionOrders:
            self.productionOrderIdGenerator.setId(po)

        self.ships = {}
        for shipId in ships:
            ship = orbitSim.transferShip(shipId)
            self.ships[shipId] = ship
            ship.locale = self

        self.vehicles = {}
        for vehicleId in vehicles:
            vehicle = locale.transferVehicle(vehicleId)
            self.vehicles[vehicleId] = vehicle

        self.crew = set()

        if locale:
            self.locale.connectColony(self)

    def wholeCrew(self):
        shipsCrew = reduce(
            set.union, 
            [ship.crew for ship in self.ships.values()], 
            set()
            )
        vehiclesCrew = reduce(
            set.union, 
            [vehicle.crew for vehicle in self.vehicles.values()], 
            set()
            )
        buildingsCrew = reduce(
            set.union,
            [building.crew for building in self.buildings.values()],
            set()
        )
        return self.crew.union(buildingsCrew).union(shipsCrew).union(vehiclesCrew)

    # Question over whether this should be given a buildingClass reference directly,
    # or just an id and look it up from colonySim. I think this should be OK even
    # though we will proliferate refs to buildingClass instances - these should all
    # be singleton objects with lifespan equal to the life of the game instance anyway,
    # and this saves an extra lookup through colonysim.
    def addBuilding(self, buildingClass: BuildingClass, colonySim=None):

        costDict = {}
        for key, value in buildingClass.constructionCost().items():
            costDict[key] = self.getResources(key, value)
            if costDict[key] < value:
                for claimedKey, claimedValue in costDict.items():
                    self.storeResources(claimedKey, claimedValue)
                return None

        id = self.buildingIdGenerator.generateId()
        if isinstance(buildingClass, ProductionBuildingClass):
            self.buildings[id] = ProductionBuilding(id, buildingClass, colonySim, locale=self)
        elif isinstance(buildingClass, StorageBuildingClass):
            self.buildings[id] = StorageBuilding(id, buildingClass, locale=self)
        elif isinstance(buildingClass, ExtractionBuildingClass):
            self.buildings[id] = ExtractionBuilding(id, buildingClass, locale=self)
        elif isinstance(buildingClass, ResearchBuildingClass):
            self.buildings[id] = ResearchBuilding(id, buildingClass, locale=self)
        elif isinstance(buildingClass, BuildingClass):
            self.buildings[id] = Building(id, buildingClass, locale=self)
        else:
            raise TypeError
    

        return id

    def productionBuildings(self):
        return [
            building
            for building in self.buildings.values()
            if isinstance(building, ProductionBuilding)
        ]

    def extractionBuildings(self):
        return [
            building
            for building in self.buildings.values()
            if isinstance(building, ExtractionBuilding)
        ]
    
    def researchBuildings(self):
        return [
            building
            for building in self.buildings.values()
            if isinstance(building, ResearchBuilding)
        ]

    def addProductionOrder(self, reaction, amount):
        id = self.productionOrderIdGenerator.generateId()
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

    def cancelProductionOrder(self, id):
        del self.productionOrders[id]

    # Try to get the full amount requested by removing it from each of our stores,
    # but if can't fully satisfy, send all that we do have.
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

    def reportResources(self, resource):
        total = 0
        for b in self.buildings.values():
            if isinstance(b, StorageBuilding) and b.contents == resource:
                total += b.amount
        return total

    def reportCapacity(self, resource):
        capacity = 0
        for b in self.buildings.values():
            if isinstance(b, StorageBuilding) and b.contents == resource:
                capacity += b.capacity()
        return capacity

    def addShip(self, name, shipClass, deltaV=0):
        shipId = self.orbitSim.createShip(name, shipClass, deltaV=deltaV)
        ship = self.orbitSim.transferShip(shipId)
        self.ships[shipId] = ship
        ship.locale = self

    def addVehicle(self, name, vehicleClass, fuel=0):
        if not self.locale and not isinstance(self.locale, PlanetSurface):
            raise TypeError
        
        vehicleId = self.vehicleFactory(name, vehicleClass, fuel)
        vehicle = self.locale.transferVehicle(vehicleId)

        self.vehicles[vehicleId] = vehicle
        return vehicleId

    def deployVehicle(self, id):
        vehicle = self.vehicleById(id)

        if isinstance(self.locale, PlanetSurface):
            position = None
            for point in self.locale.points.values():
                if point.content == self:
                    position = point.point
            if not position:
                raise KeyError

            self.locale.createSurfaceVehicle(
                None, position, name=vehicle.name, payload=vehicle
            )
            del self.vehicles[id]
        else:
            raise TypeError

    def vehicleArrival(self, vehicle):
        self.vehicles[vehicle.id] = vehicle
        return True

    def launchShip(self, ship):
        self.ships[ship.id].locale = None
        del self.ships[ship.id]

    def shipArrival(self, ship):
        self.ships[ship.id] = ship
        ship.locale = self
        return True

    def stowShip(self, ship, manifest):
        resources = {}
        for r in manifest:
            amount = self.getResources(r, manifest[r])
            resources[r] = amount
        overage = ship.addCargo(resources)
        for r in overage:
            self.storeResources(r, overage[r])

        return {key: resources[key] - overage[key] for key in manifest.keys()}

    def unloadShip(self, ship, manifest):
        resources = ship.removeCargo(manifest)
        overage = {}
        for r in resources:
            overage[r] = self.storeResources(r, resources[r])
        ship.addCargo(overage)

        return {key: resources[key] - overage[key] for key in manifest.keys()}

    def tick(self, increment):
        while increment:
            increment -= 1
            self.tickExtraction()
            self.tickProduction()
            self.tickConstruction()
            self.tickDemolition()
            self.tickResearch()

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
                # May not be the full amount, depending on what we have in stores.
                # That's OK, work with what we have.
                workingDict[i] = self.getResources(i, inputs[i] * po.amount)

            for pb in self.productionBuildings():
                if pb.status == BuildingStatus.ACTIVE and pb.reaction == po.reaction.id:
                    # Run reaction, and measure how much actually got done.
                    prior = next(iter(workingDict.values()))
                    workingDict = pb.react(workingDict, po.remaining)
                    post = next(iter(workingDict.values()))
                    # Should be 1.0 if enough resources for reaction
                    # Should just pass this as return val from react
                    ratio = (prior - post) / next(iter(inputs.values()))
                    po.remaining -= ratio
                if po.remaining <= 0:
                    break

            wastage = 0
            for r in workingDict:
                # Not all products can necessarily be stored
                # so record how much is wasted.
                wastage += self.storeResources(r, workingDict[r])

    def tickExtraction(self):
        wastage = 0
        for building in self.extractionBuildings():
            if building.status == BuildingStatus.ACTIVE:
                production = building.extract()
                wastage += self.storeResources(building.material(), production)

    def tickResearch(self):
        for building in self.researchBuildings():
            if building.status == BuildingStatus.ACTIVE:
                building.research(1)

    def tickConstruction(self):
        for building in self.buildings.values():
            if building.status == BuildingStatus.CONSTRUCTION:
                if (
                    building.constructionProgress
                    >= building.buildingClass.constructionTime()
                ):
                    self.constructBuilding(building.id)
                else:
                    building.constructionProgress += 1

        for ship in self.ships.values():
            if ship.status == ShipStatus.CONSTRUCTION:
                if (
                    ship.constructionProgress >= ship.shipClass.constructionTime()
                ):
                    ship.construct()
                else:
                    ship.constructionProgress += 1

        for vehicle in self.vehicles.values():
            if vehicle.status == VehicleStatus.CONSTRUCTION:
                if (
                    vehicle.constructionProgress
                    >= vehicle.vehicleClass.constructionTime()
                ):
                    vehicle.construct()
                else:
                    vehicle.constructionProgress += 1
                    


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

    def buildingById(self, id) -> Building:
        return getIntId(id, self.buildings)

    def productionOrderById(self, id) -> ProductionOrder:
        return getIntId(id, self.productionOrders)

    def vehicleById(self, id) -> Vehicle:
        return getIntId(id, self.vehicles)

    def shipById(self, id) -> Ship:
        return getIntId(id, self.ships)
