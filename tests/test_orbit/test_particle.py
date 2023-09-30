import unittest
from unittest.mock import MagicMock

from orbitsim.particle import Particle, DeltaVError


class TestDeltaVError(unittest.TestCase):
    def testDeltaVError(self):
        with self.assertRaises(DeltaVError):
            raise DeltaVError

    def testDeltaVErrorParam(self):
        try:
            raise DeltaVError(deltaV=5.0)
        except DeltaVError as e:
            self.assertEqual(e.deltaV, 5.0)


class MockPayload:
    pass


class TestParticle(unittest.TestCase):
    def testParticleInit(self):
        self.assertTrue(Particle)
        self.assertTrue(Particle(0))

    def testParticleAttributes(self):
        self.assertTrue(hasattr(Particle(0), "id"))
        self.assertTrue(hasattr(Particle(0), "velocity"))
        self.assertTrue(hasattr(Particle(0), "payload"))

    def testParticleConstructor(self):
        self.assertEqual(Particle(7).id, 7)
        self.assertEqual(Particle(3).velocity, 0)
        self.assertEqual(Particle(3, -1).velocity, -1)

    def testParticleDeltaVNoPayload(self):
        self.assertEqual(Particle(0).deltaV(), 0.0)

    def testParticleDeltaVPayload(self):
        payload = MockPayload()
        payload.deltaV = MagicMock(return_value=7.0)
        self.assertEqual(Particle(0, payload=payload).deltaV(), 7.0)
        payload.deltaV.assert_called_once()

    def testParticleBurnDeltaVNoPayload(self):
        with self.assertRaises(DeltaVError):
            Particle(0).burnDeltaV(10.0)

    def testParticleBurnDeltaV(self):
        pl = MockPayload()
        pl.deltaV = MagicMock(return_value=50.0)
        pl.burnDeltaV = MagicMock()
        Particle(0, payload=pl).burnDeltaV(10.0)
        pl.deltaV.assert_called_once()
        pl.burnDeltaV.assert_called_once_with(10.0)

    def testParticleBurnDeltaVInsufficient(self):
        pl = MockPayload()
        pl.deltaV = MagicMock(return_value=5.0)
        pl.burnDeltaV = MagicMock()
        with self.assertRaises(DeltaVError):
            Particle(0, payload=pl).burnDeltaV(10.0)

        try:
            Particle(1, payload=pl).burnDeltaV(10.0)
        except DeltaVError as e:
            self.assertEqual(e.deltaV, 5.0)
