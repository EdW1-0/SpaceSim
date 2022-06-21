import unittest

from planetsim.planetSurface import PlanetSurface

class TestPlanetSurface(unittest.TestCase):
    def testPlanetSurfaceModule(self):
        self.assertTrue(PlanetSurface)
        self.assertTrue(PlanetSurface())

    def testPlanetSurfaceAttributes(self):
        self.assertTrue(hasattr(PlanetSurface(), "regions"))
        self.assertTrue(hasattr(PlanetSurface(), "points"))

    def testPlanetSurfaceConstructor(self):
        self.assertTrue(PlanetSurface("test_json/test_surfaces/single_region.json"))