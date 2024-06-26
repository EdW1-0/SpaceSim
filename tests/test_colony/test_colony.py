import unittest

from colonysim import (
    ColonySim,
    Colony,
    BuildingClass,
    ProductionBuildingClass,
    StorageBuildingClass,
    ExtractionBuildingClass,
    Building,
    BuildingStatus,
    ProductionBuilding,
    StorageBuilding,
    OrderStatus,
    ShipStatus
)

from gameModel import GameModel
from planetsim import VehicleClass, Vehicle, SurfacePoint, VehicleStatus

from techtree import PlayerTech
from playerState import PlayerState


class TestColony(unittest.TestCase):
    def testColony(self):
        self.assertTrue(Colony)

    def testColonyConstructor(self):
        self.assertTrue(Colony(0, "Discovery Base"))

    def testColonyAttributes(self):
        c = Colony(0, "Default")
        self.assertTrue(hasattr(c, "id"))
        self.assertTrue(hasattr(c, "name"))
        self.assertTrue(hasattr(c, "buildings"))
        self.assertTrue(isinstance(c.buildings, dict))
        self.assertTrue(hasattr(c, "ships"))
        self.assertTrue(isinstance(c.ships, dict))
        self.assertTrue(hasattr(c, "vehicles"))
        self.assertTrue(isinstance(c.vehicles, dict))
        self.assertTrue(hasattr(c, "orbitSim"))
        self.assertTrue(hasattr(c, "locale"))
        self.assertTrue(hasattr(c, "productionOrders"))
        self.assertTrue(isinstance(c.productionOrders, dict))
        self.assertTrue(hasattr(c, "crew"))
        self.assertTrue(isinstance(c.crew, set))



class TestColonyBuildingConstruction(unittest.TestCase):
    def setUp(self):
        self.pt = PlayerTech()
        self.bc = BuildingClass("MOCK", "Mock Building", "MARTIAN")
        self.pbc = ProductionBuildingClass(
            "MOCKP", "Production", "MARTIAN", reactions={"ELECTROLYSIS": 1.0}
        )
        self.sbc = StorageBuildingClass("MOCKS", "Storage", "MARTIAN", stores={"H2O": 100})
        self.cs = ColonySim(playerTech=self.pt)

    def testColonyAddBuilding(self):
        c = Colony(0, "Default")
        self.assertEqual(c.addBuilding(self.bc), 0)
        self.assertEqual(len(c.buildings), 1)
        self.assertEqual(c.addBuilding(self.bc), 1)
        self.assertEqual(len(c.buildings), 2)
        self.assertTrue(isinstance(c.buildingById(1), Building))

    def testColonyAddStorageBuilding(self):
        c = Colony(1, "Default", buildings={})
        self.assertEqual(c.addBuilding(self.sbc), 0)
        self.assertTrue(isinstance(c.buildingById(0), StorageBuilding))

    def testColonyAddProductionBuilding(self):
        c = Colony(2, "Default", buildings={})
        self.assertEqual(c.addBuilding(self.pbc, colonySim=self.cs), 0)
        self.assertTrue(isinstance(c.buildingById(0), ProductionBuilding))

    def testColonyConstructBuilding(self):
        c = Colony(0, "Default")
        id = c.addBuilding(self.bc)
        c.constructBuilding(id)
        self.assertEqual(c.buildingById(id).status, BuildingStatus.IDLE)

    def testColonyStartBuilding(self):
        c = Colony(0, "Default")
        id = c.addBuilding(self.bc)
        c.constructBuilding(id)
        c.activateBuilding(id)
        self.assertEqual(c.buildingById(id).status, BuildingStatus.ACTIVE)

    def testColonyStopBuilding(self):
        c = Colony(0, "Default")
        id = c.addBuilding(self.bc)
        c.constructBuilding(id)
        c.activateBuilding(id)
        self.assertEqual(c.buildingById(id).status, BuildingStatus.ACTIVE)
        c.idleBuilding(id)
        self.assertEqual(c.buildingById(id).status, BuildingStatus.IDLE)

    def testColonyDemolishBuilding(self):
        c = Colony(0, "Default")
        id = c.addBuilding(self.bc)
        c.constructBuilding(id)
        c.demolishBuilding(id)
        self.assertEqual(c.buildingById(id).status, BuildingStatus.DEMOLITION)
        c.removeBuilding(id)
        with self.assertRaises(KeyError):
            c.buildingById(id)

class TestColonyBuildingCosts(unittest.TestCase):
    def setUp(self):
        self.pt = PlayerTech()
        self.bc = BuildingClass("MOCK", "Mock Building", "MARTIAN", constructionCost={"ENERGY": 1000, "AL": 100})
        self.sbc = StorageBuildingClass("STORE", "store", "MARTIAN", stores={"ENERGY": 10000, "AL": 10000})

        self.colony = Colony(0, "Default")
        self.colony.addBuilding(self.sbc)    
        self.colony.constructBuilding(0)
        self.colony.activateBuilding(0)
        self.colony.addBuilding(self.sbc)
        self.colony.constructBuilding(1)
        self.colony.activateBuilding(1)

    def testColonyBuildingCostsNoResource(self):
        self.assertIsNone(self.colony.addBuilding(self.bc))

    def testColonyBuildingCostsInsufficientResource(self):
        self.colony.buildingById(0).setContents("ENERGY")
        self.colony.buildingById(1).setContents("AL")
        self.colony.buildingById(0).add({"ENERGY":10000})
        self.colony.buildingById(1).add({"AL":50})

        self.assertIsNone(self.colony.addBuilding(self.bc))

        self.assertEqual(self.colony.reportResources("ENERGY"), 10000)
        self.assertEqual(self.colony.reportResources("AL"), 50)

    def testColonyBuildingResouceDeduction(self):
        self.colony.buildingById(0).setContents("ENERGY")
        self.colony.buildingById(1).setContents("AL")
        self.colony.buildingById(0).add({"ENERGY":10000})
        self.colony.buildingById(1).add({"AL":200})

        self.assertTrue(self.colony.addBuilding(self.bc))

        self.assertEqual(self.colony.buildingById(0).amount, 9000)
        self.assertEqual(self.colony.buildingById(1).amount, 100)




class TestColonyProductionManagement(unittest.TestCase):
    def setUp(self):
        self.cs = ColonySim(playerTech=PlayerTech())
        self.pbc = ProductionBuildingClass(
            "MOCK", "Mock", "MARTIAN", reactions={"ELECTROLYSIS": 2.0}
        )
        self.reaction = self.cs.reactionById("ELECTROLYSIS")

    def testColonyAddProductionOrder(self):
        c = Colony(0, "TEST")
        c.addProductionOrder(self.reaction, 10)
        self.assertEqual(len(c.productionOrders), 1)
        self.assertTrue(c.productionOrderById(0))

    def testColonyStartProductionOrder(self):
        c = Colony(0, "TEST")
        c.addProductionOrder(self.reaction, 10)
        self.assertEqual(c.productionOrderById(0).status, OrderStatus.PENDING)
        c.startProductionOrder(0)
        self.assertEqual(c.productionOrderById(0).status, OrderStatus.RUNNING)
        c.pauseProductionOrder(0)
        self.assertEqual(c.productionOrderById(0).status, OrderStatus.PAUSED)

    def testColonyProductionBuildings(self):
        self.sbc = StorageBuildingClass("S", "s", "MARTIAN", stores={"REGOLITH": 2000})
        self.bc = BuildingClass("B", "b", "MARTIAN")
        c = Colony(0, "TEST")
        c.addBuilding(self.bc)
        c.addBuilding(self.sbc)
        c.addBuilding(self.pbc)
        c.addBuilding(self.bc)
        c.addBuilding(self.pbc)
        c.addBuilding(self.sbc)
        self.assertEqual(len(c.productionBuildings()), 2)
        self.assertEqual(c.productionBuildings()[1].id, 4)


class TestColonyGetSetResources(unittest.TestCase):
    def setUp(self):
        self.sbc1 = StorageBuildingClass(
            "SBC1",
            "Gas", "MARTIAN",
            stores={"H2": 1000, "O2": 1000, "H2O": 1000, "He": 1000, "CO2": 1000},
        )
        self.sbc2 = StorageBuildingClass(
            "SBC2", "Ore", "MARTIAN", stores={"HEMATITE": 1000, "BAUXITE": 1000, "MALACHITE": 1000}
        )
        self.c = Colony(0, "TEST")
        for i in range(3):
            self.c.addBuilding(self.sbc1)
        for i in range(3):
            self.c.addBuilding(self.sbc2)

    def testGetResources(self):
        self.assertEqual(self.c.getResources("H2", 500), 0)
        self.c.buildingById(0).add({"H2": 600})
        self.c.buildingById(1).add({"H2": 200})
        self.c.buildingById(2).add({"H2": 400})
        self.assertEqual(self.c.getResources("H2", 100), 100)
        self.assertEqual(self.c.getResources("H2", 600), 600)
        self.assertEqual(self.c.getResources("H2", 1000), 500)

    def testGetResourcesGaps(self):
        self.c.buildingById(1).setContents("He")
        self.c.buildingById(1).add({"He": 200})
        self.c.buildingById(2).add({"H2": 300})
        self.assertEqual(self.c.getResources("H2", 300), 300)
        self.assertEqual(self.c.getResources("He", 100), 100)

    def testSetResources(self):
        self.assertEqual(self.c.storeResources("O2", 300), 300)
        self.assertEqual(self.c.storeResources("H2", 1000), 0)
        self.assertEqual(self.c.storeResources("H2", 1500), 0)
        self.assertEqual(self.c.storeResources("H2", 1000), 500)

    def testSetResourcesGaps(self):
        self.c.buildingById(1).setContents("He")
        self.c.buildingById(1).add({"He": 400})
        self.c.buildingById(0).add({"H2": 600})
        self.assertEqual(self.c.storeResources("He", 1000), 400)
        self.assertEqual(self.c.storeResources("H2", 2000), 600)
        self.assertEqual(self.c.buildingById(1).amount, 1000)


class TestColonyReportResources(unittest.TestCase):
    def setUp(self):
        self.sbc1 = StorageBuildingClass(
            "SBC1",
            "Gas", "MARTIAN",
            stores={"H2": 1000, "O2": 1000, "H2O": 1000, "He": 1000, "CO2": 1000},
        )
        self.sbc2 = StorageBuildingClass(
            "SBC2", "Ore", "MARTIAN", stores={"HEMATITE": 1000, "BAUXITE": 1000, "MALACHITE": 1000}
        )
        self.c = Colony(0, "TEST")
        for i in range(3):
            self.c.addBuilding(self.sbc1)
        for i in range(3):
            self.c.addBuilding(self.sbc2)

    def testReportEmpty(self):
        self.assertEqual(self.c.reportResources("H2"), 0)

    def testReportSingle(self):
        self.c.buildingById(0).setContents("H2O")
        self.c.storeResources("H2O", 500)
        self.assertEqual(self.c.reportResources("H2O"), 500)
        self.assertEqual(self.c.reportResources("CO2"), 0)

    def testReportMultiple(self):
        self.c.buildingById(0).setContents("H2O")
        self.c.buildingById(2).setContents("H2O")
        self.c.storeResources("H2O", 700)
        self.c.storeResources("H2", 600)
        self.c.storeResources("H2O", 800)
        self.assertEqual(self.c.reportResources("H2O"), 1500)
        self.assertEqual(self.c.reportResources("H2"), 600)

    def testReportCapacityEmpty(self):
        self.assertEqual(self.c.reportCapacity("H2O"), 0)
        self.assertEqual(self.c.reportCapacity("H2"), 3000)


class TestColonyTick(unittest.TestCase):
    def setUp(self):
        self.cs = ColonySim(playerTech=PlayerTech())
        self.pbc = ProductionBuildingClass(
            "MOCK", "Mock", "MARTIAN", reactions={"ELECTROLYSIS": 2.0}
        )
        self.sbc = StorageBuildingClass(
            "SBC", "Sbc", "MARTIAN", stores={"H2": 1000, "O2": 1000, "H2O": 1000}
        )
        self.sbce = StorageBuildingClass("SBCE", "Battery", "MARTIAN", stores={"ENERGY": 100000})
        self.reaction = self.cs.reactionById("ELECTROLYSIS")
        self.c = Colony(0, "TEST")
        self.c.addProductionOrder(self.reaction, 100)
        self.c.addBuilding(self.pbc, self.cs)
        self.c.addBuilding(self.sbc)
        self.c.addBuilding(self.sbc)
        self.c.addBuilding(self.sbc)
        self.c.addBuilding(self.sbce)
        for i in range(5):
            self.c.buildingById(i).construct()
            self.c.buildingById(i).start()
        self.c.buildingById(0).setReaction("ELECTROLYSIS")
        self.c.buildingById(1).setContents("H2")
        self.c.buildingById(2).setContents("O2")
        self.c.buildingById(3).setContents("H2O")
        self.c.buildingById(3).add({"H2O": 500})
        self.c.buildingById(4).add({"ENERGY": 5000})

    def testColonyTickOrderPending(self):
        po = self.c.productionOrderById(0)
        self.assertEqual(po.status, OrderStatus.PENDING)
        self.assertEqual(po.remaining, 100)
        self.c.tick(10)
        self.assertEqual(po.remaining, 100)

    def testColonyTickOrderPaused(self):
        po = self.c.productionOrderById(0)
        self.c.startProductionOrder(po.id)
        self.c.pauseProductionOrder(po.id)
        self.assertEqual(po.status, OrderStatus.PAUSED)
        self.assertEqual(po.remaining, 100)
        self.c.tick(10)
        self.assertEqual(po.remaining, 100)

    def testColonyTickRunning(self):
        po = self.c.productionOrderById(0)
        self.c.startProductionOrder(po.id)
        self.assertEqual(po.remaining, 100)
        self.c.tick(1)
        self.assertEqual(po.remaining, 98)
        self.assertEqual(self.c.getResources("H2O", 10000), 496.0)
        self.assertEqual(self.c.getResources("H2", 50), 4.0)

    def testColonyTickFractionalPO(self):
        po = self.c.productionOrderById(0)
        po.remaining = 1
        self.c.startProductionOrder(po.id)
        self.c.tick(1)
        self.assertEqual(po.remaining, 0)
        self.assertEqual(self.c.getResources("H2", 50), 2.0)
        self.assertEqual(self.c.getResources("H2O", 10000), 498.0)

    def testColonyTickMultiple(self):
        po = self.c.productionOrderById(0)
        self.c.startProductionOrder(po.id)
        self.c.tick(5)
        self.assertEqual(po.remaining, 90)
        self.assertEqual(self.c.getResources("H2", 50), 20.0)
        self.assertEqual(self.c.getResources("H2O", 10000), 480.0)


class TestColonyTickExtraction(unittest.TestCase):
    def setUp(self):
        self.sbc = StorageBuildingClass("BATTERY", "Battery", "MARTIAN", stores={"ENERGY": 10000})
        self.ebc = ExtractionBuildingClass(
            "SOLAR", "Solar Array", "MARTIAN", extracts={"ENERGY": 100}
        )

    def testColonyTickExtract(self):
        self.c = Colony(0, "Test")
        self.c.addBuilding(self.sbc)
        self.c.addBuilding(self.ebc)
        self.c.constructBuilding(0)
        self.c.constructBuilding(1)
        self.c.buildingById(0).start()
        self.c.buildingById(1).start()
        self.assertEqual(self.c.buildingById(0).amount, 0)
        self.c.tick(1)
        self.assertEqual(self.c.buildingById(0).amount, 100)
        self.c.addBuilding(self.ebc)
        self.c.addBuilding(self.ebc)
        self.c.constructBuilding(2)
        self.c.constructBuilding(3)
        self.c.buildingById(3).start()
        self.c.tick(1)
        self.assertEqual(self.c.buildingById(0).amount, 300)
        self.c.tick(10)
        self.assertEqual(self.c.buildingById(0).amount, 2300)


class TestColonyTickConstruction(unittest.TestCase):
    def setUp(self):
        class PT:
            def addResearch(self, amount):
                pass
        self.pt = PlayerState()
        self.bc = BuildingClass("MOCK", "Mock Building", "MARTIAN", constructionTime=20, playerState=self.pt)
        self.pbc = ProductionBuildingClass(
            "MOCKP", "Production", "MARTIAN", playerState=self.pt, reactions={"ELECTROLYSIS": 1.0}
        )
        self.sbc = StorageBuildingClass("MOCKS", "Storage", "MARTIAN", stores={"H2O": 100}, playerState=self.pt)
        self.cs = ColonySim(playerTech=PT())

    def testColonyTickConstruction(self):
        self.c = Colony(0, "Test")
        self.c.addBuilding(self.pbc, self.cs)
        self.c.addBuilding(self.sbc)
        self.c.addBuilding(self.bc)
        for i in range(3):
            self.assertEqual(self.c.buildingById(i).constructionProgress, 0)
        self.c.tick(1)
        for i in range(3):
            self.assertEqual(self.c.buildingById(i).constructionProgress, 1)

        self.c.tick(3)
        for i in range(3):
            self.assertEqual(self.c.buildingById(i).constructionProgress, 4)
            self.assertEqual(self.c.buildingById(i).status, BuildingStatus.CONSTRUCTION)

        self.c.tick(10)
        for i in range(2):
            self.assertEqual(self.c.buildingById(i).constructionProgress, 10)
            self.assertEqual(self.c.buildingById(i).status, BuildingStatus.IDLE)
        self.assertEqual(self.c.buildingById(2).constructionProgress, 14)
        self.assertEqual(self.c.buildingById(2).status, BuildingStatus.CONSTRUCTION)


class TestColonyTickDemolition(unittest.TestCase):
    def setUp(self):
        self.pt = PlayerState()

        self.bc = BuildingClass("MOCK", "Mock Building", "MARTIAN", demolitionTime=20, playerState=self.pt)
        self.pbc = ProductionBuildingClass(
            "MOCKP", "Production", "MARTIAN", reactions={"ELECTROLYSIS": 1.0}, playerState=self.pt
        )
        self.sbc = StorageBuildingClass("MOCKS", "Storage", "MARTIAN", stores={"H2O": 100}, playerState=self.pt)
        self.cs = ColonySim(playerState=self.pt, playerTech=PlayerTech())

    def testColonyTickDemolition(self):
        self.c = Colony(0, "Test")
        self.c.addBuilding(self.pbc, self.cs)
        self.c.addBuilding(self.sbc)
        self.c.addBuilding(self.bc)
        self.c.tick(25)
        for i in range(3):
            self.assertEqual(self.c.buildingById(i).status, BuildingStatus.IDLE)
        self.c.demolishBuilding(0)
        self.c.demolishBuilding(2)
        self.assertEqual(self.c.buildingById(0).status, BuildingStatus.DEMOLITION)
        self.assertEqual(self.c.buildingById(2).status, BuildingStatus.DEMOLITION)
        self.assertEqual(self.c.buildingById(0).demolitionProgress, 0)
        self.assertEqual(self.c.buildingById(2).demolitionProgress, 0)
        self.c.tick(1)
        self.assertEqual(self.c.buildingById(0).demolitionProgress, 1)
        self.assertEqual(self.c.buildingById(2).demolitionProgress, 1)
        self.assertEqual(self.c.buildingById(1).demolitionProgress, 0)
        self.c.tick(10)
        self.assertEqual(self.c.buildingById(2).demolitionProgress, 11)
        with self.assertRaises(KeyError):
            self.c.buildingById(0)
        self.c.tick(20)
        with self.assertRaises(KeyError):
            self.c.buildingById(2)


class testColonyShip(unittest.TestCase):
    def setUp(self):
        self.gm = GameModel()
        self.gm.load()
        self.sc = self.gm.orbitSim.shipClassById("SATURNVI")

    def testColonyAddShip(self):
        self.c = Colony(0, "TEST", self.gm.orbitSim)
        self.c.addShip("Test ship", self.sc, deltaV=56)
        self.assertGreater(len(self.c.ships), 0)
        self.assertEqual(self.c.ships[5].shipClass, self.sc)
        self.assertEqual(self.c.ships[5].deltaV(), 56)

    def testColonyLoadShip(self):
        colony = self.gm.colonySim.colonyById(0)
        ship = colony.shipById(4)
        retDict = colony.stowShip(ship, {"H2": 100, "H2O": 20})
        self.assertEqual(retDict["H2"], 0)
        self.assertEqual(retDict["H2O"], 20)
        with self.assertRaises(KeyError):
            ship.cargo["H2"]
        self.assertEqual(ship.cargo["H2O"], 20)
        self.assertEqual(colony.reportResources("H2"), 0)
        self.assertEqual(colony.reportResources("H2O"), 180)

    def testColonyUnloadShip(self):
        colony = self.gm.colonySim.colonyById(0)
        ship = colony.shipById(4)
        ship.addCargo({"ENERGY": 500, "H2O": 200, "CHEESE": 200})
        retDict = colony.unloadShip(ship, {"ENERGY": 300, "H2O": 500, "CHEESE": 200})
        self.assertEqual(retDict["ENERGY"], 300)
        self.assertEqual(retDict["H2O"], 200)
        self.assertEqual(retDict["CHEESE"], 0)
        self.assertEqual(ship.cargo["ENERGY"], 200)
        with self.assertRaises(KeyError):
            ship.cargo["H2O"]
        self.assertEqual(ship.cargo["CHEESE"], 200)
        self.assertEqual(colony.reportResources("ENERGY"), 6300)
        self.assertEqual(colony.reportResources("H2O"), 400)
        self.assertEqual(colony.reportResources("CHEESE"), 0)

    def testColonyShipConstruction(self):
        self.c = Colony(0, "TEST", self.gm.orbitSim)
        self.c.addShip("Test ship", self.sc, deltaV=56)
        ship = self.c.shipById(5)
        self.assertEqual(ship.status, ShipStatus.CONSTRUCTION)
        self.assertEqual(ship.constructionProgress, 0)
        self.c.tick(1)
        self.assertEqual(ship.constructionProgress, 1)

        self.c.tick(7)
        self.assertEqual(ship.constructionProgress, 8)

        self.c.tick(int(ship.shipClass.constructionTime()))
        self.assertEqual(ship.constructionProgress, ship.shipClass.constructionTime())
        self.assertEqual(ship.status, ShipStatus.IDLE)


class testColonyVehicle(unittest.TestCase):
    def setUp(self):
        self.gm = GameModel()
        self.gm.load()
        self.ps = self.gm.planetSim.planetById("MERCURY").surface
        self.ps.createBase(None, SurfacePoint(30, 30), "Foo", 3)
        self.state = PlayerState()
        self.vc = VehicleClass("ROLLER", "Roller", playerState=self.state, constructionTime=30)

    def testColonyAddVehicle(self):
        self.c = Colony(0, "TEST", self.gm.orbitSim, self.ps, vehicleFactory=self.gm.planetSim.createVehicle)
        self.assertFalse(2 in self.gm.planetSim.vehicles)
        self.assertEqual(self.c.addVehicle("Test vehicle", self.vc, fuel=100), 2)
        self.assertGreater(len(self.c.vehicles), 0)
        self.assertTrue(2 in self.gm.planetSim.vehicles)

    def testColonyDeployVehicle(self):
        self.c = Colony(3, "TEST", self.gm.orbitSim, self.ps, vehicleFactory=self.gm.planetSim.createVehicle)
        self.ps.connectColony(self.c)
        id = self.c.addVehicle("Test vehicle", self.vc, fuel=100)
        self.assertEqual(len(self.c.vehicles), 1)
        self.assertEqual(len(self.ps.points), 4)
        self.c.deployVehicle(id)
        self.assertEqual(len(self.c.vehicles), 0)
        self.assertEqual(len(self.ps.points), 5)

    def testColonyVehicleArrival(self):
        self.c = Colony(4, "TEST", self.gm.orbitSim, self.ps)
        self.ps.connectColony(self.c)
        self.assertEqual(len(self.c.vehicles), 0)
        v = Vehicle(99, "Test Vehicle", self.vc, 60)
        self.assertTrue(self.c.vehicleArrival(v))
        self.assertEqual(len(self.c.vehicles), 1)


    def testVehicleConstruction(self):
        self.c = Colony(0, "TEST", self.gm.orbitSim, self.ps, vehicleFactory=self.gm.planetSim.createVehicle)
        self.c.addVehicle("Test vehicle", self.vc, fuel=100)
        vehicle = self.c.vehicleById(2)
        self.assertEqual(vehicle.constructionProgress, 0)
        self.assertEqual(vehicle.status, VehicleStatus.CONSTRUCTION)

        self.c.tick(100) 
        self.assertEqual(vehicle.status, VehicleStatus.IDLE)
        self.assertEqual(vehicle.constructionProgress, 30)

class TestColonyCrew(unittest.TestCase):
    def setUp(self):
        self.gm = GameModel()
        self.gm.load()
        self.sc = self.gm.orbitSim.shipClassById("SATURNVI")
        self.vc = self.gm.planetSim.vehicleClassById("ROVER")
        self.c = Colony(0, 
                        "TEST", 
                        self.gm.orbitSim, 
                        locale=self.gm.planetSim.planetById("MERCURY").surface,
                        vehicleFactory=self.gm.planetSim.createVehicle)
        self.bc = BuildingClass("MOCK", "Mock Building", "MARTIAN", constructionTime=20)

    def testColonyCrew(self):
        self.assertSetEqual(self.c.wholeCrew(), set())
        self.c.crew.add(7)
        self.c.crew.add(2)
        self.assertSetEqual(self.c.wholeCrew(), {7, 2})

    def testColonyShipsCrew(self):
        self.c.crew.add(2)
        self.c.crew.add(4)
        self.assertSetEqual(self.c.wholeCrew(), {2, 4})
        self.c.addShip("Test ship", self.sc, deltaV=56)
        self.c.shipById(5).crew.add(7)
        self.c.shipById(5).crew.add(9)
        self.c.addShip("Test ship 2", self.sc, deltaV=56)
        self.c.shipById(6).crew.add(12)

        self.assertSetEqual(self.c.wholeCrew(), {2, 4, 7, 9, 12})

    def testColonyVehiclesCrew(self):
        self.c.crew.add(2)
        self.c.crew.add(4)
        self.assertSetEqual(self.c.wholeCrew(), {2, 4})
        self.c.addVehicle("Test vehicle", self.vc, fuel=100)
        self.c.vehicleById(2).crew.add(7)
        self.c.vehicleById(2).crew.add(9)
        self.c.addVehicle("Test vehicle 2", self.vc, fuel=100)
        self.c.vehicleById(3).crew.add(12)

        self.assertSetEqual(self.c.wholeCrew(), {2, 4, 7, 9, 12})

    def testColonyBuildingsCrew(self):
        self.c.crew.add(2)
        self.assertSetEqual(self.c.wholeCrew(), {2})
        self.c.addBuilding(self.bc)
        self.c.addBuilding(self.bc)
        self.c.buildingById(0).crew.add(3)
        self.c.buildingById(0).crew.add(7)
        self.c.buildingById(1).crew.add(9)

        self.assertSetEqual(self.c.wholeCrew(), {2, 3, 7, 9})

 

