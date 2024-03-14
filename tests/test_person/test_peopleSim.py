import unittest

from peoplesim.peopleSim import PeopleSim

class CMock:
    def __init__(self, id):
        self.id = id
        self.crew = set()

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
        self.assertEqual(self.peopleSim.createPerson("John Doe", 30, "M", self.os.shipById(5)), 6)
        self.assertEqual(self.peopleSim.personById(6).name, "John Doe")
        self.assertEqual(self.peopleSim.personById(6).location.id, 5)
        self.assertTrue(isinstance(self.peopleSim.personById(6).location, SMock))
        self.assertIn(6, self.os.shipById(5).crew)

    def testPeopleSimDestroyPerson(self):
        self.peopleSim.destroyPerson(1)
        with self.assertRaises(KeyError):
            self.peopleSim.personById(1)

        self.assertEqual(self.peopleSim.createPerson("John Doe", 30, "M", self.os.shipById(5)), 6)
        self.assertEqual(self.peopleSim.personById(6).name, "John Doe")
        self.peopleSim.destroyPerson(6)
        with self.assertRaises(KeyError):
            self.peopleSim.personById(6)


    def testPeopleSimTransferPerson(self):
        self.peopleSim.transferPerson(self.peopleSim.personById(1), self.os.shipById(5))
        self.assertEqual(self.peopleSim.personById(1).location.id, 5)
        self.assertIsInstance(self.peopleSim.personById(1).location, SMock)
