import unittest

from orbitsim.orbitTrajectory import OrbitTrajectory

class TestOrbitTrajectory(unittest.TestCase):
    def testOrbitTrajectory(self):
        self.assertTrue(OrbitTrajectory)
        self.assertTrue(OrbitTrajectory(0, []))

class TestOrbitTrajectoryAttributes(unittest.TestCase):
    def testOrbitTrajectoryAttributes(self):
        self.assertTrue(hasattr(OrbitTrajectory(0, []), "particleId"))
        self.assertTrue(hasattr(OrbitTrajectory(0, []), "trajectory"))
        
class TestOrbitTrajectoryConstructor(unittest.TestCase):
    def testOrbitTrajectoryConstructor(self):
        self.assertTrue(OrbitTrajectory(0, [0, 0, 1]))
