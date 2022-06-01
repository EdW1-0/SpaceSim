import unittest

from orbitsim.particle import Particle

class TestParticle(unittest.TestCase):
    def testParticleInit(self):
        self.assertTrue(Particle)
        self.assertTrue(Particle())

    def testParticleAttributes(self):
        self.assertTrue(hasattr(Particle(), "mass"))