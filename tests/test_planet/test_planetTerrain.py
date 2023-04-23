import unittest

from planetsim.planetTerrain import PlanetTerrain

class TestPlanetTerrain(unittest.TestCase):
    def testPlanetTerrain(self):
        self.assertTrue(PlanetTerrain)

    def testPlanetTerrainConstructor(self):
        with self.assertRaises(TypeError):
            PlanetTerrain()
        self.assertTrue(PlanetTerrain(id = "TESTID"))
        self.assertTrue(PlanetTerrain(id = "TESTID", name = "Cheese terrain", colour = (200, 200, 50)))

    def testPlanetTerrainAttributes(self):
        pt = PlanetTerrain(id = "TESTID")
        self.assertTrue(hasattr(pt, "id"))
        self.assertTrue(hasattr(pt, "name"))
        self.assertTrue(hasattr(pt, "colour"))
