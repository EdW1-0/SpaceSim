import unittest

from orbitsim.orbitTrajectory import OrbitTrajectory
from planetsim.surfacePoint import SurfacePoint

class TestOrbitTrajectory(unittest.TestCase):
    def testOrbitTrajectory(self):
        self.assertTrue(OrbitTrajectory)
        self.assertTrue(OrbitTrajectory(0, []))

class TestOrbitTrajectoryAttributes(unittest.TestCase):
    def testOrbitTrajectoryAttributes(self):
        self.assertTrue(hasattr(OrbitTrajectory(0, []), "particleId"))
        self.assertTrue(hasattr(OrbitTrajectory(0, []), "trajectory"))
        self.assertTrue(hasattr(OrbitTrajectory(0, []), "state"))
        self.assertTrue(hasattr(OrbitTrajectory(0, [], surfaceCoordinates = SurfacePoint(10, 10)), "surfaceCoordinates"))
        
class TestOrbitTrajectoryConstructor(unittest.TestCase):
    def testOrbitTrajectoryConstructor(self):
        self.assertTrue(OrbitTrajectory(0, [0, 0, 1]))
        
class TestOrbitTrajectoryUtilities(unittest.TestCase):
    def setUp(self):
        self.ot = OrbitTrajectory(0, [3,5,4,8,5,9,9])
    def testOrbitTrajectoryNextLink(self):
        self.assertEqual(self.ot.nextLink(3), 5)
        self.assertEqual(self.ot.nextLink(5), 9)
    def testOrbitTrajectoryNextNode(self):
        self.assertEqual(self.ot.nextNode(5), 4)
        self.assertEqual(self.ot.nextNode(9), 9)

