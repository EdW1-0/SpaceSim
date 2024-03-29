import unittest

from colonysim import ColonySim, ProductionBuildingClass, ShipClass



class MockLocale:
    def connectColony(self, colony):
        pass


class TestColonySim(unittest.TestCase):
    def testColonySim(self):
        self.assertTrue(ColonySim)

    def testColonySimConstructor(self):
        self.assertTrue(ColonySim())
        self.assertTrue(ColonySim(resourcePath="json/resources"))
        self.assertTrue(ColonySim(reactionPath="json/reactions"))
        self.assertTrue(ColonySim(buildingPath="json/buildingClasses"))

    def testColonySimAttributes(self):
        cs = ColonySim()
        self.assertTrue(hasattr(cs, "_buildingClasses"))
        self.assertTrue(hasattr(cs, "_resources"))
        self.assertTrue(hasattr(cs, "_reactions"))
        self.assertTrue(hasattr(cs, "_colonies"))
        self.assertTrue(isinstance(cs._buildingClasses, dict))
        self.assertTrue(isinstance(cs._resources, dict))
        self.assertTrue(isinstance(cs._reactions, dict))
        self.assertTrue(isinstance(cs._colonies, dict))

    def testColonySimLoading(self):
        cs = ColonySim()
        self.assertTrue(len(cs._resources.values()) > 0)
        self.assertTrue(len(cs._reactions.values()) > 0)
        self.assertTrue(len(cs._buildingClasses.values()) > 0)
        self.assertTrue(
            isinstance(cs._buildingClasses["REACTOR"], ProductionBuildingClass)
        )

        csr = ColonySim(resourcePath="test_json/test_colony/test_resources")
        self.assertEqual(len(csr._resources.values()), 2)
        self.assertEqual(csr._resources["RAD"].units, "g")
        self.assertEqual(csr._resources["HE3"].baseValue, 10000.0)

        csrc = ColonySim(reactionPath="test_json/test_colony/test_reactions")
        self.assertEqual(len(csrc._reactions.values()), 2)
        self.assertEqual(csrc._reactions["ELECTROLYSIS"].inputs["H2O"], 2)
        self.assertEqual(csrc._reactions["SABATIER"].outputs["CH4"], 1)

        csb = ColonySim(buildingPath="test_json/test_colony/test_buildingClasses")
        self.assertEqual(len(csb._buildingClasses.values()), 2)
        self.assertEqual(csb._buildingClasses["HAB"].baseConstructionTime, 30)
        self.assertEqual(csb._buildingClasses["SOL"].baseConstructionCost, 200.0)

    def testColonySimCreateColony(self):
        cs = ColonySim()
        locale = MockLocale()
        self.assertEqual(len(cs._colonies.values()), 0)
        self.assertEqual(cs.createColony("Hadley's Hope", locale=locale).id, 0)
        self.assertEqual(len(cs._colonies.values()), 1)
        self.assertEqual(cs.createColony("Freedom's Progress", locale=locale).id, 1)


class TestColonySimObjectLookup(unittest.TestCase):
    def setUp(self):
        self.cs = ColonySim()

    def testColonySimReactionById(self):
        self.assertTrue(self.cs.reactionById("SABATIER"))
        self.assertEqual(self.cs.reactionById("SABATIER").inputs, {"CO2": 1, "H2O": 2})

class TestColonySimBuildingClassFiltering(unittest.TestCase):
    def setUp(self):
        class PlayerTechMock:
            def __init__(self):
                self.discoveredBuildings = {"BUILDING", "HAB"}
            def addResearch(self, amount):
                pass

        self.cs = ColonySim(playerTech=PlayerTechMock())

    def testColonySimBuildingClassFiltering(self):
        self.assertTrue("HAB" in self.cs.buildingClassesForColony("NOTAREALCOLONY"))
        self.assertFalse("SOLARARRAY" in self.cs.buildingClassesForColony("NOTAREALCOLONY"))

class TestColonySimShipClassFiltering(unittest.TestCase):
    def setUp(self):
        class PlayerTechMock:
            def __init__(self):
                self.discoveredShips = {"SATURNVI"}
            def addResearch(self, amount):
                pass

        class OrbitSimMock:
            def __init__(self):
                self._shipClasses = {"SATURNVI": ShipClass("SATURNVI", "Saturn VI", maxDeltaV=100),
                                     "SOLARSAIL": ShipClass("SOLARSAIL", "Solar Sail", maxDeltaV=1000)}

        self.cs = ColonySim(orbitSim=OrbitSimMock(), playerTech=PlayerTechMock())

    def testColonySimShipClassFiltering(self):
        self.assertTrue("SATURNVI" in self.cs.shipClassesForColony("NOTAREALCOLONY"))
        self.assertFalse("SOLARSAIL" in self.cs.shipClassesForColony("NOTAREALCOLONY"))