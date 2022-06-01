import unittest

from orbitsim.orbitSim import OrbitSim

class TestOrbitSim(unittest.TestCase):
    def testOrbitSim(self):
        self.assertNotEqual(OrbitSim, False)
        self.assertTrue(OrbitSim())

    def testOrbitSimParticles(self):
        self.assertTrue(hasattr(OrbitSim(), "_particles"))