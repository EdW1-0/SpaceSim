import unittest
from unittest.mock import MagicMock

from peoplesim.peopleSim import PeopleSim
from colonysim import BuildingStatus

class CMock:
    def __init__(self, id):
        self.id = id
        self.crew = set()
        self.buildings = {}
    
    def buildingById(self, id: int):
        if not id in self.buildings:
            self.buildings[id] = BMock(id)

        return self.buildings[id]
    
class BMock:
    def __init__(self, id):
        self.id = id
        self.crew = set()
        self.buildingStatus = BuildingStatus.CONSTRUCTION

class CSMock:
    def __init__(self):
        self._colonies = {}
    def colonyById(self, id: int):
        if not id in self._colonies:
            self._colonies[id] = CMock(id)
            
        return self._colonies[id]

class SMock:
    def __init__(self, id):
        self.id = id
        self.crew = set()

class OSMock:
    def __init__(self):
        self._ships = {}
    def shipById(self, id: int):
        if not id in self._ships:
            self._ships[id] = SMock(id)
            
        return self._ships[id]
    
class VMock:
    def __init__(self, id):
        self.id = id
        self.crew = set()

class PSMock:
    def __init__(self):
        self.vehicles = {}
    def vehicleById(self, id: int):
        if not id in self.vehicles:
            self.vehicles[id] = VMock(id)
            
        return self.vehicles[id]



class TestPeopleSim(unittest.TestCase):
    def setUp(self):
        self.cs = CSMock()
        self.os = OSMock()
        self.ps = PSMock()

    def testPeopleSim(self):
        self.assertTrue(PeopleSim)
        self.assertTrue(PeopleSim(colonySim=self.cs, orbitSim=self.os, planetSim=self.ps))

    def testPeopleSimConstructor(self):
        self.assertTrue(PeopleSim(jsonPath="test_json/test_people", colonySim=self.cs, orbitSim=self.os, planetSim=self.ps))

    def testPeopleSimAttributes(self):
        self.assertTrue(hasattr(PeopleSim(colonySim=self.cs, orbitSim=self.os, planetSim=self.ps), "_people"))
        self.assertTrue(hasattr(PeopleSim(colonySim=self.cs, orbitSim=self.os, planetSim=self.ps), "_taskClasses"))

    def testPeopleSimPersonById(self):
        self.assertTrue(PeopleSim(colonySim=self.cs, orbitSim=self.os, planetSim=self.ps).personById(1))


class TestPeopleSimLoading(unittest.TestCase):
    def setUp(self):     
        self.cs = CSMock()
        self.os = OSMock()
        self.ps = PSMock()
        self.peopleSim = PeopleSim(
            jsonPath="test_json/test_people", 
            colonySim=self.cs, 
            orbitSim=self.os, 
            planetSim=self.ps
            )

    def testPeopleSimBasicBiographics(self):
        self.assertEqual(self.peopleSim.personById(1).name, "Jane Doe")
        self.assertEqual(self.peopleSim.personById(1).age, 24)
        self.assertEqual(self.peopleSim.personById(1).sex, "F")

    def testPeopleSimLocationLoadModifier(self):
        self.assertEqual(self.peopleSim.locationLoadModifier(location = 0, locationClass = "Colony").id, 0)
        self.assertTrue(isinstance(self.peopleSim.locationLoadModifier(location = 0, locationClass = "Colony"), CMock))
        self.assertEqual(self.peopleSim.locationLoadModifier(location = 2, locationClass = "Colony").id, 2)
        self.assertTrue(isinstance(self.peopleSim.locationLoadModifier(location = [2,4], locationClass = "Colony"), BMock))

        with self.assertRaises(ValueError):
            self.peopleSim.locationLoadModifier(location = 0, locationClass = "Planet")

    def testPeopleSimLocationLoadModifierShipAndVehicle(self):
        self.assertEqual(self.peopleSim.locationLoadModifier(location = 0, locationClass = "Ship").id, 0)
        self.assertTrue(isinstance(self.peopleSim.locationLoadModifier(location = 0, locationClass = "Ship"), SMock))   

        self.assertEqual(self.peopleSim.locationLoadModifier(location = 0, locationClass = "Vehicle").id, 0)
        self.assertTrue(isinstance(self.peopleSim.locationLoadModifier(location = 0, locationClass = "Vehicle"), VMock))

    def testPeopleSimLocationLinking(self):
        self.assertEqual(self.peopleSim.personById(1).location.id, 0)
        self.assertEqual(self.peopleSim.personById(2).location.id, 2)
        self.assertTrue(1 in self.cs.colonyById(0).crew)
        self.assertTrue(2 in self.cs.colonyById(2).crew)
        
        self.assertEqual(self.peopleSim.personById(4).location.id, 1)
        self.assertTrue(4 in self.os.shipById(1).crew)

        self.assertEqual(self.peopleSim.personById(5).location.id, 3)
        self.assertTrue(5 in self.ps.vehicleById(3).crew)

        self.assertEqual(self.peopleSim.personById(6).location.id, 3)
        self.assertTrue(6 in self.cs.colonyById(2).buildingById(3).crew)


class TestPeopleSimLifecycle(unittest.TestCase):
    def setUp(self) -> None:
        self.cs = CSMock()
        self.os = OSMock()
        self.ps = PSMock()
        self.peopleSim = PeopleSim(
            jsonPath="test_json/test_people", 
            colonySim=self.cs, 
            orbitSim=self.os, 
            planetSim=self.ps
            )
        
    def testPeopleSimCreatePerson(self):
        self.assertEqual(self.peopleSim.createPerson("John Doe", 30, "M", self.os.shipById(5)), 7)
        self.assertEqual(self.peopleSim.personById(7).name, "John Doe")
        self.assertEqual(self.peopleSim.personById(7).location.id, 5)
        self.assertTrue(isinstance(self.peopleSim.personById(7).location, SMock))
        self.assertIn(7, self.os.shipById(5).crew)

    def testPeopleSimDestroyPerson(self):
        self.peopleSim.destroyPerson(1)
        with self.assertRaises(KeyError):
            self.peopleSim.personById(1)

        self.assertEqual(self.peopleSim.createPerson("John Doe", 30, "M", self.os.shipById(5)), 7)
        self.assertEqual(self.peopleSim.personById(7).name, "John Doe")
        self.peopleSim.destroyPerson(7)
        with self.assertRaises(KeyError):
            self.peopleSim.personById(7)


    def testPeopleSimTransferPerson(self):
        self.peopleSim.transferPerson(self.peopleSim.personById(1), self.os.shipById(5))
        self.assertEqual(self.peopleSim.personById(1).location.id, 5)
        self.assertIsInstance(self.peopleSim.personById(1).location, SMock)

        self.peopleSim.transferPerson(self.peopleSim.personById(1), self.ps.vehicleById(3))
        self.assertEqual(self.peopleSim.personById(1).location.id, 3)
        self.assertIsInstance(self.peopleSim.personById(1).location, VMock)

        self.peopleSim.transferPerson(self.peopleSim.personById(1), self.cs.colonyById(2))
        self.assertEqual(self.peopleSim.personById(1).location.id, 2)
        self.assertIsInstance(self.peopleSim.personById(1).location, CMock)

        self.peopleSim.transferPerson(self.peopleSim.personById(1), self.cs.colonyById(2).buildingById(3))
        self.assertEqual(self.peopleSim.personById(1).location.id, 3)   
        self.assertIsInstance(self.peopleSim.personById(1).location, BMock)


class TestPeopleSimTaskLifecycle(unittest.TestCase):
    def setUp(self) -> None:
        self.cs = CSMock()
        self.os = OSMock()
        self.ps = PSMock()
        self.peopleSim = PeopleSim(
            jsonPath="test_json/test_people", 
            colonySim=self.cs, 
            orbitSim=self.os, 
            planetSim=self.ps
            )

    def testPeopleSimTaskCreation(self):
        mockPerson = MagicMock()
        self.assertEqual(len(self.peopleSim.taskQueue), 0)
        self.peopleSim.createTask("IDLE", target=mockPerson)
        self.assertEqual(len(self.peopleSim.taskQueue), 1)

    def testPeopleSimTaskById(self):
        mockPerson = MagicMock()
        self.assertEqual(len(self.peopleSim.taskQueue), 0)
        self.peopleSim.createTask("IDLE", target=mockPerson)
        self.assertEqual(self.peopleSim.taskById(0).taskClass.id, "IDLE")

    def testPeopleSimTaskAssignment(self):
        mockPerson = MagicMock()
        self.peopleSim.createTask("IDLE", target=mockPerson)
        task = self.peopleSim.taskById(0)
        person = self.peopleSim.personById(1)
        self.peopleSim.assignTask(task, person)
        self.assertEqual(self.peopleSim.taskQueue[0].assigneeId, 1)
        self.assertEqual(person.task, task)

        self.peopleSim.createTask("IDLE", target=mockPerson)
        task2 = self.peopleSim.taskById(1)
        self.peopleSim.assignTask(task2, person)
        self.assertIsNone(task.assigneeId)
        self.assertEqual(person.task, task2)

        person2 = self.peopleSim.personById(2)
        self.peopleSim.assignTask(task2, person2)
        self.assertIsNone(person.task)

    def testPeopleSimTaskCompletion(self):
        mockPerson = MagicMock()
        self.peopleSim.createTask("BUILD", target=mockPerson)
        task = self.peopleSim.taskById(0)
        self.peopleSim.assignTask(task, self.peopleSim.personById(1))
        self.assertEqual(self.peopleSim.personById(1).task.taskClass.id, "BUILD")
        self.assertEqual(self.peopleSim.taskQueue[0].assigneeId, 1)
        self.peopleSim.completeTask(task)
        self.assertIsNone(self.peopleSim.personById(1).task)
        self.assertEqual(len(self.peopleSim.taskQueue), 0)

    def testPeopleSimTaskCompleteBuilding(self):
        mockPerson = MagicMock()
        building = self.cs.colonyById(0).buildingById(0)
        self.peopleSim.createTask("BUILD", target=building)
        task = self.peopleSim.taskById(0)
        self.peopleSim.assignTask(task, self.peopleSim.personById(1))
        self.assertEqual(building.buildingStatus, "CONSTRUCTION")
        self.peopleSim.completeTask(task)
        self.assertEqual(building.buildingStatus, "IDLE")

class TestPeopleSimTick(unittest.TestCase):
    def setUp(self) -> None:
        self.cs = CSMock()
        self.os = OSMock()
        self.ps = PSMock()
        self.peopleSim = PeopleSim(
            jsonPath="test_json/test_people", 
            colonySim=self.cs, 
            orbitSim=self.os, 
            planetSim=self.ps
            )
        
    def testPeopleSimTick(self):
        self.peopleSim.createTask("BUILD", target=self.peopleSim.personById(1))
        task = self.peopleSim.taskById(0)
        self.peopleSim.tick()
        self.assertTrue(self.peopleSim.personById(0).task.taskClass.id == "BUILD")

        self.assertEqual(self.peopleSim.personById(0).task, task)
        self.assertEqual(task.assigneeId, 0)
        self.assertEqual(task.progress, 1)

        for i in range(1, 10):
            self.peopleSim.tick()
        
        self.assertEqual(len(self.peopleSim.taskQueue), 0)
        self.assertIsNone(self.peopleSim.personById(0).task)