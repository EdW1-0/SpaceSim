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



class TestPeopleSim(unittest.TestCase):
    def setUp(self):
        self.cs = CSMock()
        self.os = OSMock()

    def testPeopleSim(self):
        self.assertTrue(PeopleSim)
        self.assertTrue(PeopleSim(colonySim=self.cs, orbitSim=self.os))

    def testPeopleSimConstructor(self):
        self.assertTrue(PeopleSim(jsonPath="test_json/test_people", colonySim=self.cs, orbitSim=self.os))

    def testPeopleSimAttributes(self):
        self.assertTrue(hasattr(PeopleSim(colonySim=self.cs, orbitSim=self.os), "_people"))

    def testPeopleSimPersonById(self):
        self.assertTrue(PeopleSim(colonySim=self.cs, orbitSim=self.os).personById(1))


class TestPeopleSimLoading(unittest.TestCase):
    def setUp(self):     
        self.cs = CSMock()
        self.os = OSMock()
        self.peopleSim = PeopleSim(jsonPath="test_json/test_people", colonySim=self.cs, orbitSim=self.os)

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

        with self.assertRaises(NotImplementedError):
            self.peopleSim.locationLoadModifier(location = 0, locationClass = "Vehicle")

    def testPeopleSimLocationLinking(self):
        self.assertEqual(self.peopleSim.personById(1).location.id, 0)
        self.assertEqual(self.peopleSim.personById(2).location.id, 2)
        self.assertTrue(1 in self.cs.colonyById(0).crew)
        self.assertTrue(2 in self.cs.colonyById(2).crew)
        
        self.assertEqual(self.peopleSim.personById(4).location.id, 1)
        self.assertTrue(4 in self.os.shipById(1).crew)

