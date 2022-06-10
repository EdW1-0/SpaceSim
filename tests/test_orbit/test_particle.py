import unittest

from orbitsim.particle import Particle

class TestParticle(unittest.TestCase):
    def testParticleInit(self):
        self.assertTrue(Particle)
        self.assertTrue(Particle(0))

    def testParticleAttributes(self):
        self.assertTrue(hasattr(Particle(0), "id"))

    
