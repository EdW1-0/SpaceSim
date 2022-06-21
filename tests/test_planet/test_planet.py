import unittest

from planetsim.planet import Planet

class SurfaceMock:
    pass

class AtmosphereMock:
    pass

class TestPlanet(unittest.TestCase):
    def testPlanetModule(self):
        self.assertTrue(Planet)
        self.assertTrue(Planet(0.0))

    def testPlanetAttributes(self):
        self.assertTrue(hasattr(Planet(0.0), "surface"))
        self.assertTrue(hasattr(Planet(0.0), "atmosphere"))
        self.assertTrue(hasattr(Planet(0.0), "gravity"))

    def testPlanetConstructor(self):
        self.assertTrue(Planet(7.0))
        self.assertTrue(Planet(gravity = 6.0))
        self.assertEqual(Planet(gravity = 5.0).gravity, 5.0)
        self.assertTrue(Planet(gravity = 3.0, surface = SurfaceMock()))
        sm = SurfaceMock()
        self.assertEqual(Planet(gravity = 1.0, surface = sm).surface, sm)
        self.assertTrue(Planet(gravity = 2.0, surface = sm, atmosphere = AtmosphereMock()))
        am = AtmosphereMock()
        self.assertEqual(Planet(gravity = 3.0, surface = sm, atmosphere = am).atmosphere, am)