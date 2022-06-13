import unittest

from orbitsim.particle import Particle

class TestParticle(unittest.TestCase):
    def testParticleInit(self):
        self.assertTrue(Particle)
        self.assertTrue(Particle(0))

    def testParticleAttributes(self):
        self.assertTrue(hasattr(Particle(0), "id"))
        self.assertTrue(hasattr(Particle(0), "velocity"))

    def testParticleConstructor(self):
        self.assertEqual(Particle(7).id, 7)
        self.assertEqual(Particle(3).velocity, 0)
        self.assertEqual(Particle(3, -1).velocity, -1)

    
