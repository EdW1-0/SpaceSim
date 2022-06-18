import unittest

from planetsim.planet import Planet

class TestPlanet(unittest.TestCase):
    def testPlanetModule(self):
        self.assertTrue(Planet)
        self.assertTrue(Planet())