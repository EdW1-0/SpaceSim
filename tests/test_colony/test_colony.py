import unittest

from colonysim.colony import Colony
from colonysim.buildingClass import BuildingClass, ProductionBuildingClass, StorageBuildingClass, ExtractionBuildingClass
from colonysim.building import Building, BuildingStatus, ProductionBuilding, StorageBuilding
from colonysim.colonySim import ColonySim
from gameModel import GameModel
from colonysim.productionOrder import OrderStatus

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

class TestColonyBuildingConstruction(unittest.TestCase):
    def setUp(self):
        self.bc = BuildingClass("MOCK", "Mock Building")
        self.pbc = ProductionBuildingClass("MOCKP", "Production", reactions={"ELECTROLYSIS": 1.0})
        self.sbc = StorageBuildingClass("MOCKS", "Storage", stores={"H2O": 100})
        self.cs = ColonySim()

    def testColonyAddBuilding(self):
        c = Colony(0, "Default")
        self.assertEqual(c.addBuilding(self.bc), 0)
        self.assertEqual(len(c.buildings), 1)
        self.assertEqual(c.addBuilding(self.bc), 1)
        self.assertEqual(len(c.buildings), 2)
        self.assertTrue(isinstance(c.buildingById(1), Building))
    
    def testColonyAddStorageBuilding(self):
        c = Colony(0, "Default")
        self.assertEqual(c.addBuilding(self.sbc), 0)
        self.assertTrue(isinstance(c.buildingById(0), StorageBuilding))

    def testColonyAddProductionBuilding(self):
        c = Colony(0, "Default")
        self.assertEqual(c.addBuilding(self.pbc, colonySim = self.cs), 0)
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

class TestColonyProductionManagement(unittest.TestCase):
    def setUp(self):
        self.cs = ColonySim()
        self.pbc = ProductionBuildingClass("MOCK", "Mock", reactions={"ELECTROLYSIS": 2.0})
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
        self.sbc = StorageBuildingClass("S", "s", stores={"REGOLITH": 2000})
        self.bc = BuildingClass("B", "b")
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
        self.sbc1 = StorageBuildingClass("SBC1", "Gas", stores={"H2": 1000, "O2": 1000, "H2O": 1000, "He": 1000, "CO2": 1000})
        self.sbc2 = StorageBuildingClass("SBC2", "Ore", stores={"HEMATITE": 1000, "BAUXITE": 1000, "MALACHITE": 1000})
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

    

class TestColonyTick(unittest.TestCase):
    def setUp(self):
        self.cs = ColonySim()
        self.pbc = ProductionBuildingClass("MOCK", "Mock", reactions={"ELECTROLYSIS": 2.0})
        self.sbc = StorageBuildingClass("SBC", "Sbc", stores={"H2": 1000, "O2": 1000, "H2O": 1000})
        self.sbce = StorageBuildingClass("SBCE", "Battery", stores={"ENERGY": 100000})
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
        self.sbc = StorageBuildingClass("BATTERY", "Battery", stores={"ENERGY": 10000})
        self.ebc = ExtractionBuildingClass("SOLAR", "Solar Array", extracts={"ENERGY": 100})

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
        self.bc = BuildingClass("MOCK", "Mock Building", constructionTime=20)
        self.pbc = ProductionBuildingClass("MOCKP", "Production", reactions={"ELECTROLYSIS": 1.0})
        self.sbc = StorageBuildingClass("MOCKS", "Storage", stores={"H2O": 100})
        self.cs = ColonySim()

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
        self.bc = BuildingClass("MOCK", "Mock Building", demolitionTime=20)
        self.pbc = ProductionBuildingClass("MOCKP", "Production", reactions={"ELECTROLYSIS": 1.0})
        self.sbc = StorageBuildingClass("MOCKS", "Storage", stores={"H2O": 100})
        self.cs = ColonySim()

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
        self.c.addShip("Test ship", self.sc, deltaV = 56)
        self.assertGreater(len(self.c.ships), 0)
        self.assertEqual(self.c.ships[4].shipClass, self.sc)
        self.assertEqual(self.c.ships[4].deltaV(), 56)
        
class testColonyVehicle(unittest.TestCase):
    def setUp(self):
        self.gm = GameModel()
        self.gm.load()
        self.ps = self.gm.planetSim.planetById("MERCURY").surface

    def testColonyAddVehicle(self):
        self.c = Colony(0, "TEST", self.gm.orbitSim, self.ps)
        self.c.addVehicle("Test vehicle", fuel = 100, maxV = 10)
        self.assertGreater(len(self.c.vehicles), 0)




          
