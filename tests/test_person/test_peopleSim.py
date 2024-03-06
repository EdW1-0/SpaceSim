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




class TestPeopleSim(unittest.TestCase):
    def setUp(self):
        self.cs = CSMock()

    def testPeopleSim(self):
        self.assertTrue(PeopleSim)
        self.assertTrue(PeopleSim(colonySim=self.cs))

    def testPeopleSimConstructor(self):
        self.assertTrue(PeopleSim(jsonPath="test_json/test_people", colonySim=self.cs))

    def testPeopleSimAttributes(self):
        self.assertTrue(hasattr(PeopleSim(colonySim=self.cs), "_people"))

    def testPeopleSimPersonById(self):
        self.assertTrue(PeopleSim(colonySim=self.cs).personById(1))


class TestPeopleSimLoading(unittest.TestCase):
    def setUp(self):     
        self.cs = CSMock()
        self.peopleSim = PeopleSim(jsonPath="test_json/test_people", colonySim=self.cs)

    def testPeopleSimBasicBiographics(self):
        self.assertEqual(self.peopleSim.personById(1).name, "Jane Doe")
        self.assertEqual(self.peopleSim.personById(1).age, 24)
        self.assertEqual(self.peopleSim.personById(1).sex, "F")

    def testPeopleSimLocationLoadModifier(self):
        self.assertEqual(self.peopleSim.locationLoadModifier(location = 0, locationClass = "Colony").id, 0)
        self.assertEqual(self.peopleSim.locationLoadModifier(location = 2, locationClass = "Colony").id, 2)

        with self.assertRaises(ValueError):
            self.peopleSim.locationLoadModifier(location = 0, locationClass = "Planet")

    def testPeopleSimLocationLoadModifierShipAndVehicle(self):
        with self.assertRaises(NotImplementedError):
            self.peopleSim.locationLoadModifier(location = 0, locationClass = "Ship")

        with self.assertRaises(NotImplementedError):
            self.peopleSim.locationLoadModifier(location = 0, locationClass = "Vehicle")

    def testPeopleSimLocationLinking(self):
        self.assertEqual(self.peopleSim.personById(1).location.id, 0)
        self.assertEqual(self.peopleSim.personById(2).location.id, 2)
        self.assertTrue(1 in self.cs.colonyById(0).crew)
        self.assertTrue(2 in self.cs.colonyById(2).crew)

