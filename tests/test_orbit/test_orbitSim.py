import unittest

import json

from orbitsim.orbitSim import OrbitSim
from orbitsim.particle import DeltaVError, Particle
from orbitsim.orbitTrajectory import OrbitTrajectory, TrajectoryState

class PayloadMock:
    def __init__(self, deltaV):
        self.dV = deltaV

    def deltaV(self):
        return self.dV 

    def burnDeltaV(self, dv):
        self.dV -= dv

class TestOrbitSim(unittest.TestCase):
    def testOrbitSim(self):
        self.assertNotEqual(OrbitSim, False)
        self.assertTrue(OrbitSim())

    def testOrbitSimParticles(self):
        self.assertTrue(hasattr(OrbitSim(), "_particles"))
        self.assertTrue(hasattr(OrbitSim(), "_nodes"))
        self.assertTrue(hasattr(OrbitSim(), "_links"))
        self.assertTrue(hasattr(OrbitSim(), "_shipClasses"))

    def testOrbitSimLoad(self):
        self.assertTrue(OrbitSim("test_json/test_orbits/happy_case.json"))
        with self.assertRaises(FileNotFoundError):
            OrbitSim("test_json/test_orbits/nonexistant.json")
        with self.assertRaises(json.JSONDecodeError):
            OrbitSim("test_json/test_orbits/malformed.json")
        self.assertNotEqual(OrbitSim("test_json/test_orbits/happy_case.json")._nodes, [])
        self.assertNotEqual(OrbitSim("test_json/test_orbits/happy_case.json")._nodes, {})
        self.assertEqual(len(OrbitSim("test_json/test_orbits/happy_case.json")._nodes), 4)
        self.assertEqual(len(OrbitSim("test_json/test_orbits/happy_case.json")._links), 3)
        with self.assertRaises(KeyError):
            OrbitSim("test_json/test_orbits/duplicate.json")
        self.assertGreater(len(OrbitSim()._shipClasses), 0)
        self.assertGreater(len(OrbitSim()._ships), 0)

    def testOrbitSimParticleLoad(self):
        os = OrbitSim(particlePath = "json/Particles.json")
        self.assertEqual(len(os._particles.values()), 4)

        
class TestOrbitSimNodes(unittest.TestCase):
    def setUp(self):
        self.os = OrbitSim("test_json/test_orbits/happy_case.json")

    def testOrbitSimNodeById(self):
        self.assertTrue(self.os.nodeById(0))
        with self.assertRaises(ValueError):
            OrbitSim().nodeById("Sun")
        with self.assertRaises(TypeError):
            OrbitSim().nodeById(6.31)
        with self.assertRaises(TypeError):
            OrbitSim().nodeById(True)
        with self.assertRaises(TypeError):
            OrbitSim().nodeById([])
    
    def testOrbitSimNode0(self):
        n0 = self.os.nodeById(0)
        self.assertEqual(n0.id, 0)
        self.assertEqual(n0.name, "Sun")

    def testOrbitSimNode1(self):
        n1 = self.os.nodeById(1)
        self.assertEqual(n1.id, 1)
        self.assertEqual(n1.name, "Sun Low Orbit")

class TestOrbitSimLinks(unittest.TestCase):
    def setUp(self):
        self.os = OrbitSim("test_json/test_orbits/happy_case.json")

    def testOrbitSimLinkById(self):
        self.assertTrue(self.os.linkById(0))
        with self.assertRaises(TypeError):
            OrbitSim().linkById("Sun")
        with self.assertRaises(ValueError):
            OrbitSim().linkById(-1)

    def testOrbitSimLinkage(self):
        self.assertEqual(self.os.linkById(0).topNode, 1)
        self.assertEqual(self.os.linkById(0).bottomNode, 0)
        self.assertEqual(self.os.nodeById(0).links, [0, 1])
        self.assertEqual(self.os.nodeById(1).links, [0, 2])

    def testOrbitSimLinkageMultidrop(self):
        self.assertTrue(self.os.linkById(1))
        self.assertEqual(self.os.linkById(1).topNode, 3)
        self.assertEqual(self.os.linkById(1).bottomNode, 0)
        self.assertEqual(self.os.nodeById(3).links, [1])
        
    def testOrbitSimMultiLink(self):
        self.assertTrue(self.os.linkById(2))
        self.assertEqual(self.os.linkById(2).topNode, 2)
        self.assertEqual(self.os.linkById(2).bottomNode, 1)
        self.assertEqual(self.os.nodeById(1).links, [0, 2])
        self.assertEqual(self.os.nodeById(2).links, [2])

class TestOrbitSimIdLookup(unittest.TestCase):
    def setUp(self):
        self.os = OrbitSim(particlePath="json/Particles.json")

    def testOrbitSimParticleById(self):
        self.assertEqual(self.os.particleById(0).id, 0)

    def testOrbitSimShipClassById(self):
        self.assertEqual(self.os.shipClassById("SATURNVI").name, "Saturn VI")

    def testOrbitSimShipById(self):
        self.assertEqual(self.os.shipById(0).name, "ISS Meghalaya")

class TestOrbitSimProperties(unittest.TestCase):
    def setUp(self):
        self.os = OrbitSim("test_json/test_orbits/happy_case.json")

    def testOrbitSimLink0(self):
        l0 = self.os.linkById(0)
        self.assertEqual(l0.deltaV, 1000)
        self.assertEqual(l0.travelTime, 10000)
        self.assertEqual(l0.distance, 100000)

    def testOrbitSimLink1(self):
        l1 = self.os.linkById(1)
        self.assertEqual(l1.deltaV, 500)
        self.assertEqual(l1.travelTime, 100000)
        self.assertEqual(l1.distance, 200000)

    def testOrbitSimLinkAll(self):
        for l in self.os._links.values():
            self.assertGreater(l.deltaV, 0)
            self.assertGreater(l.travelTime, 0)
            self.assertGreater(l.travelTime, 0)

class TestOrbitSimParticleCreation(unittest.TestCase):
    def setUp(self):
        self.os = OrbitSim("test_json/test_orbits/happy_case.json")
        self.n0 = self.os.nodeById(0)
        self.os.createParticle(self.n0)
        self.os.createParticle(self.n0)

    def testOrbitSimParticleCreationLength(self):
        self.assertEqual(len(self.n0.particles), 2)
        self.assertEqual(len(self.os._particles), 2)

    def testOrbitSimParticleCreationTypes(self):
        for p in self.os._particles.values():
            self.assertTrue(isinstance(p, Particle))
        for p in self.n0.particles:
            self.assertFalse(isinstance(p, Particle))

    def testOrbitSimParticleCreationIds(self):
        for i in (0, 1):
            self.assertTrue(i in self.n0.particles)
        for i in (0, 1):
            self.assertTrue(i in self.os._particles.keys())
            self.assertEqual(self.os._particles[i].id, i)

    def testOrbitSimParticleCreationReturnValue(self):
        n1 = self.os.nodeById(1)
        for i in range(5):
            self.assertEqual(self.os.createParticle(n1), i+2)


class TestOrbitSimParticleDestruction(unittest.TestCase):
    def setUp(self):
        self.os = OrbitSim("test_json/test_orbits/happy_case.json")
        self.n0 = self.os.nodeById(0)
        self.l0 = self.os.linkById(0)
        for i in range(10):
            self.os.createParticle(self.n0)

    def testOrbitSimParticleDestructionNode(self):
        self.os.destroyParticle(2)
        self.assertEqual(len(self.os._particles), 9)
        with self.assertRaises(KeyError):
            self.os._particleLocation(2)
        self.assertFalse(2 in self.n0.particles)

        self.os.destroyParticle(3)
        self.assertEqual(len(self.os._particles), 8)
        with self.assertRaises(KeyError):
            self.os._particleLocation(3)
        self.assertFalse(3 in self.n0.particles)

        self.os.createParticle(self.n0)
        self.assertEqual(len(self.os._particles), 9)
        try:
            self.os.particleById(10)
        except KeyError:
            self.fail("particleById threw KeyError for id 20!")
        self.assertEqual(self.os.particleById(10).id, 10)


class TestOrbitSimParticleTransit(unittest.TestCase):
    def setUp(self):
        self.os = OrbitSim("test_json/test_orbits/happy_case.json")
        self.n0 = self.os.nodeById(0)
        self.l0 = self.os.linkById(0)
        for i in range(10):
            self.os.createParticle(self.n0)

    def testOrbitSimParticleTransitToLink(self):
        self.os.transitParticle(0, self.l0.id)
        self.assertTrue(0 in self.l0.particles)
        self.assertTrue(0 not in self.n0.particles)

    def testOrbitSimParticleTransitToNode(self):
        self.os.transitParticle(1, self.l0.id)
        self.os.transitParticle(1, self.n0.id)
        self.assertTrue(1 in self.n0.particles)
        self.assertTrue(1 not in self.l0.particles)

    def testOrbitSimParticleTransitFullClimb(self):
        self.os.transitParticle(1, self.l0.id)
        self.os.transitParticle(1, 1)
        self.assertTrue(1 in self.os.nodeById(1).particles)
        self.assertEqual(self.os.particleById(1).velocity, 0)

    def testOrbitSimParticleTransitInvalidParticle(self):
        with self.assertRaises(KeyError):
            self.os.transitParticle(30, self.n0.id)

    def testOrbitSimParticleTransitInvalidTarget(self):
        with self.assertRaises(KeyError):
            self.os.transitParticle(1, 50)

    def testOrbitSimParticleTransitUnconnectedLink(self):
        with self.assertRaises(ValueError):
            self.os.transitParticle(0, 2)

    def testOrbitSimParticleTransitUnconnectedNode(self):
        self.os.transitParticle(2, 0)
        with self.assertRaises(ValueError):
            self.os.transitParticle(2, 2)

    def testOrbitSimParticleTransitInvariants(self):
        self.assertEqual(len(self.os._particles), 10)
        self.os.transitParticle(0, 0)
        self.os.transitParticle(3, 1)
        self.assertEqual(len(self.os._particles), 10)
        self.assertEqual(len(self.n0.particles), 8)
        self.assertEqual(len(self.l0.particles), 1)
        self.assertEqual(len(self.os.linkById(1).particles), 1)

class TestOrbitSimParticleTravel(unittest.TestCase):
    def setUp(self):
        self.os = OrbitSim("test_json/test_orbits/happy_case.json")
        self.n0 = self.os.nodeById(0)
        self.l0 = self.os.linkById(0)
        for i in range(10):
            self.os.createParticle(self.n0)

    def testOrbitSimParticleTravelUp(self):
        self.os.transitParticle(0,0)
        self.assertEqual(self.os.particleById(0).velocity, 1)
        self.assertEqual(self.l0.particles[0], 0)

    def testOrbitSimParticleTravelDown(self):
        self.os.transitParticle(1, 0)
        self.os.transitParticle(1, 1)
        self.os.transitParticle(1, 0)
        self.assertEqual(self.os.particleById(1).velocity, -1)
        self.assertEqual(self.l0.particles[1], self.l0.travelTime)


class TestOrbitSimTick(unittest.TestCase):
    def setUp(self):
        self.os = OrbitSim("test_json/test_orbits/happy_case.json")
        self.n0 = self.os.nodeById(0)
        self.l0 = self.os.linkById(0)
        for i in range(10):
            self.os.createParticle(self.n0)

        
    def testOrbitSimTickUpMotion(self):
        self.os.createTrajectory(targetId = 1, particleId = 1, initialState=TrajectoryState.ACTIVE)
        self.os.transitParticle(1, 0)
        self.os.tick(100)
        self.assertEqual(self.l0.particles[1], 100)

    def testOrbitSimTickDownMotion(self):
        self.os.transitParticle(5, 0)
        self.os.transitParticle(5, 1)
        self.os.createTrajectory(particleId = 5, targetId = 0, initialState = TrajectoryState.ACTIVE)
        self.os.transitParticle(5, 0)
        self.os.tick(300)
        self.assertEqual(self.l0.particles[5], self.l0.travelTime - 300)

    def testOrbitSimTickUpMulti(self):
        self.os.createTrajectory(1, particleId = 2, initialState = TrajectoryState.ACTIVE)
        self.os.transitParticle(2, 0)
        self.os.createTrajectory(3, particleId = 3, initialState = TrajectoryState.ACTIVE)
        self.os.transitParticle(3, 1)
        self.os.transitParticle(1, 0)
        self.os.transitParticle(1, 1)
        self.os.createTrajectory(0, particleId = 1, initialState = TrajectoryState.ACTIVE)
        self.os.transitParticle(1, 0)
        self.os.tick(30)
        self.os.tick(50)
        self.os.tick(110)
        self.assertEqual(self.l0.particles[2], 190)
        self.assertEqual(self.os.linkById(1).particles[3], 190)
        self.assertEqual(self.l0.particles[1], self.l0.travelTime - 190)

class TestOrbitSimParticleArrival(unittest.TestCase):
    def setUp(self):
        self.os = OrbitSim("test_json/test_orbits/happy_case.json")
        self.n0 = self.os.nodeById(0)
        self.l0 = self.os.linkById(0)
        for i in range(10):
            self.os.createParticle(self.n0)

    def testOrbitSimTopArrival(self):
        self.os.createTrajectory(1, particleId = 2, initialState = TrajectoryState.ACTIVE)
        self.os.transitParticle(2, 0)
        self.os.tick(self.l0.travelTime + 100)
        self.assertTrue(2 in self.os.nodeById(1).particles)
        self.assertEqual(self.os.particleById(2).velocity, 0)

    def testOrbitSimBottomArrival(self):
        self.os.transitParticle(6, 0)
        self.os.transitParticle(6, 1)
        self.os.createTrajectory(0, particleId = 6, initialState = TrajectoryState.ACTIVE)
        self.os.transitParticle(6, 0)
        self.os.tick(self.l0.travelTime + 100)
        self.assertTrue(6 in self.n0.particles)
        self.assertEqual(self.os.particleById(6).velocity, 0)

class TestOrbitSimTrajectoryState(unittest.TestCase):
    def setUp(self):
        self.os = OrbitSim("test_json/test_orbits/happy_case.json")
        pl = PayloadMock(deltaV = 100000.0)
        self.os.createParticle(self.os.nodeById(0), payload = pl)

    def testOrbitSimTrajectoryDefinition(self):
        self.os.createTrajectory(1, sourceId = 0, particleId=0)
        self.assertEqual(self.os.trajectoryForParticle(0).state, TrajectoryState.DEFINITION)
        self.os.tick(1e6)
        self.assertEqual(self.os.particleById(0).deltaV(), 100000.0)
        self.assertTrue(0 in self.os.nodeById(0).particles)

    def testOrbitSimTrajectoryPending(self):
        self.os.createTrajectory(1, sourceId = 0, particleId = 0, initialState = TrajectoryState.PENDING)
        self.assertEqual(self.os.trajectoryForParticle(0).state, TrajectoryState.PENDING)
        self.os.tick(100)
        self.assertEqual(self.os.trajectoryForParticle(0).state, TrajectoryState.ACTIVE)
        self.assertFalse(0 in self.os.nodeById(0).particles)

    def testOrbitSimTrajectoryActive(self):
        self.os.createTrajectory(1, sourceId = 0, particleId = 0, initialState = TrajectoryState.ACTIVE)
        self.assertEqual(self.os.trajectoryForParticle(0).state, TrajectoryState.ACTIVE)
        self.os.tick(100)
        self.assertFalse(0 in self.os.nodeById(0).particles)

    def testOrbitSimTrajectoryComplete(self):
        self.os.createTrajectory(1, sourceId = 0, particleId = 0, initialState = TrajectoryState.COMPLETE)
        self.assertEqual(self.os.trajectoryForParticle(0).state, TrajectoryState.COMPLETE)
        self.os.tick(100)
        with self.assertRaises(KeyError):
            self.os.trajectoryForParticle(0)
        



class TestOrbitSimFindPath(unittest.TestCase):
    def setUp(self):
        self.os = OrbitSim("test_json/test_orbits/happy_case.json")
        self.ucos = OrbitSim("test_json/test_orbits/unconnected.json")
        self.los = OrbitSim("test_json/test_orbits/loops.json")
        self.udos = OrbitSim("test_json/test_orbits/up_down.json")


    def testOrbitSimFindPath1Hop(self):
        self.assertEqual(self.os._findPath(0, 1, []), [[0,0,1]])

    def testOrbitSimFindPath2Hop(self):
        self.assertEqual(self.os._findPath(0, 2, []), [[0,0,1,2,2]])

    def testOrbitSimFindPathUnconnected(self):
        self.assertEqual(self.ucos._findPath(0, 2, []), [[0,0,1,1,2]])
        self.assertEqual(self.ucos._findPath(3, 4, []), [[3,2,4]])
        self.assertEqual(self.ucos._findPath(0, 3, []), [])

    def testOrbitSimLoops(self):
        self.assertEqual(self.los._findPath(0, 3, []), [[0,0,1,2,2,3,3],[0,1,3]])
        self.assertEqual(self.los._findPath(3, 4, []), [[3, 4, 4], [3,5,4], [3,6,4]])
        self.assertEqual(self.los._findPath(0, 4, []), [[0,0,1,2,2,3,3,4,4],[0,0,1,2,2,3,3,5,4],[0,0,1,2,2,3,3,6,4],[0,1,3,4,4],[0,1,3,5,4],[0,1,3,6,4]])

    def testOrbitSimUpDown(self):
        self.assertEqual(self.udos._findPath(0, 10, []), [[0,0,1,1,2,2,3,4,7,7,8,9,9,10,10]])
        self.assertEqual(self.udos._findPath(6, 10, []), [[6,6,5,5,4,3,3,4,7,7,8,9,9,10,10]])

class TestOrbitSimTrajectory(unittest.TestCase):
    def setUp(self):
        self.os = OrbitSim("test_json/test_orbits/happy_case.json")
        self.n0 = self.os.nodeById(0)
        self.l0 = self.os.linkById(0)
        for i in range(10):
            pl = PayloadMock(10000.0)
            self.os.createParticle(self.n0, payload = pl)

        self.ucos = OrbitSim("test_json/test_orbits/unconnected.json")
        self.los = OrbitSim("test_json/test_orbits/loops.json")
        self.udos = OrbitSim("test_json/test_orbits/up_down.json")

    def testOrbitSimTrajectoryCreationExistingParticle(self):
        self.assertTrue(self.os.createTrajectory(targetId = 2, particleId = 0))
        self.assertIsInstance(self.os.createTrajectory(targetId = 2, particleId = 1), OrbitTrajectory)
        self.assertEqual(self.os.createTrajectory(targetId = 2, particleId = 2).particleId, 2)
        

    def testOrbitSimTrajectoryCreationNewParticle(self):
        t = self.os.createTrajectory(targetId = 0, sourceId = 2, payload = PayloadMock(30.0))
        self.assertTrue(t)
        self.assertIsInstance(t, OrbitTrajectory)

        self.assertTrue(self.os.particleById(t.particleId))
        self.assertEqual(self.os._particleLocation(t.particleId).id, 2)

    def testOrbitSimTrajectoryCreationException(self):
        with self.assertRaises(ValueError):
            self.os.createTrajectory(targetId = 1, payload = PayloadMock(20.0))

    def testOrbitSimTrajectory1Hop(self):
        self.assertEqual(self.os.createTrajectory(targetId = 1, particleId = 0).trajectory, [0,0,1])

    def testOrbitSimTrajectoryNoncontiguous(self):
        self.assertEqual(self.ucos.createTrajectory(targetId = 2, sourceId = 0).trajectory, [0,0,1,1,2])
        self.assertEqual(self.ucos.createTrajectory(targetId = 4, sourceId = 3).trajectory, [3,2,4])
        with self.assertRaises(ValueError):
            self.ucos.createTrajectory(targetId = 3, sourceId = 0)

    def testOrbitSimTrajectoryDeltaV(self):
        self.assertEqual(self.los.createTrajectory(targetId = 3, sourceId = 0).trajectory, [0,1,3])

    def testOrbitSimTrajectoryRetrieval(self):
        self.os.createTrajectory(targetId = 1, sourceId = 0)
        self.os.createTrajectory(targetId = 2, sourceId = 0)
        self.assertEqual(self.os.trajectoryForParticle(10).trajectory, [0,0,1])
        self.assertEqual(self.os.trajectoryForParticle(11).trajectory, [0,0,1,2,2])

    def testOrbitSimTrajectoryExistingTrajectory(self):
        self.os.createTrajectory(targetId = 1, particleId = 0)
        with self.assertRaises(KeyError):
            self.os.createTrajectory(targetId = 2, particleId = 0)

    def testOrbitSimTrajectoryTimeStep(self):
        self.os.createTrajectory(targetId = 1, particleId = 0, initialState=TrajectoryState.ACTIVE)
        self.os.tick(100)
        self.assertTrue(0 in self.os.linkById(0).particles)
        self.assertEqual(self.os.linkById(0).particles[0], 100)

    def testOrbitSimTrajectoryFullLink(self):
        self.os.createTrajectory(targetId = 1, particleId = 0, initialState=TrajectoryState.ACTIVE)
        self.os.tick(10100)
        self.assertTrue(0 in self.os.nodeById(1).particles)

    def testOrbitSimMultiHop(self):
        self.udos.createTrajectory(targetId = 9, sourceId = 0, payload = PayloadMock(10000.0), initialState=TrajectoryState.ACTIVE)
        self.udos.tick(1000)
        self.assertTrue(0 in self.udos.nodeById(9).particles)

    def testOrbitSimMultiHopDown(self):
        self.udos.createTrajectory(targetId = 0, sourceId = 9, payload = PayloadMock(10000.0), initialState=TrajectoryState.ACTIVE)
        self.udos.tick(1000)
        self.assertTrue(0 in self.udos.nodeById(0).particles)

    def testOrbitSimMultiHopPartial(self):
        self.udos.createTrajectory(targetId = 10, sourceId = 6, payload = PayloadMock(10000.0), initialState=TrajectoryState.ACTIVE)
        self.udos.tick(65)
        self.assertTrue(0 in self.udos.linkById(10).particles)
        self.assertEqual(self.udos.linkById(10).particles[0], 5)

    def testOrbitSimPruneCompletedTrajectories(self):
        self.os.createTrajectory(1, sourceId = 0, payload = PayloadMock(10000.0), initialState=TrajectoryState.ACTIVE)
        self.os.createTrajectory(2, sourceId = 0, payload = PayloadMock(10000.0), initialState=TrajectoryState.ACTIVE)
        self.assertEqual(len(self.os._trajectories), 2)
        self.os.tick(1e6)
        self.assertEqual(len(self.os._trajectories), 1)

    def testOrbitSimCancelTrajectory(self):
        self.os.createTrajectory(2, sourceId = 0, payload = PayloadMock(10000.0), initialState=TrajectoryState.ACTIVE)
        self.os.tick(5000)
        self.os.createTrajectory(2, sourceId = 0, payload = PayloadMock(10000.0), initialState=TrajectoryState.ACTIVE)
        self.assertEqual(len(self.os._trajectories), 2)
        self.os.cancelTrajectory(11)
        self.assertEqual(len(self.os._trajectories), 1)
        self.os.cancelTrajectory(10)
        self.assertEqual(len(self.os._trajectories), 1)
        self.assertEqual(self.os.trajectoryForParticle(10).trajectory, [0, 0, 1])
        self.os.tick(6000)
        self.assertEqual(len(self.os._trajectories), 0)
        
    def testOrbitSimCancelNonexistant(self):
        try:
            self.os.cancelTrajectory(0)
        except:
            self.fail("Unexpected exception thrown on cancelling nonexistant trajectory")

class TestOrbitSimDeltaVBudget(unittest.TestCase):
    def setUp(self):
        self.udos = OrbitSim("test_json/test_orbits/up_down.json")
        self.n0 = self.udos.nodeById(0)
        self.l0 = self.udos.linkById(0)
        for i in range(10):
            pl = PayloadMock(deltaV = 50.0)
            self.udos.createParticle(self.n0, payload = pl)

    def testOrbitSimDeltaVSingleHop(self):
        self.udos.createTrajectory(1, particleId = 0, initialState = TrajectoryState.ACTIVE)
        self.assertEqual(self.udos.particleById(0).deltaV(), 50.0)
        self.udos.tick(5)
        self.assertTrue(0 in self.l0.particles)
        self.assertEqual(self.udos.particleById(0).deltaV(), 40.0)

    def testOrbitSimDeltaVMultiHop(self):
        self.udos.createTrajectory(6, sourceId = 0, payload = PayloadMock(100.0), initialState = TrajectoryState.ACTIVE)
        self.assertEqual(self.udos.particleById(10).deltaV(), 100.0)
        self.udos.tick(100)
        self.assertEqual(self.udos.particleById(10).deltaV(), 40.0)
        self.assertTrue(10 in self.udos.nodeById(6).particles)

    def testOrbitSimDeltaVInsufficientDeltaV(self):
        self.udos.createTrajectory(10, particleId = 3, initialState = TrajectoryState.ACTIVE)
        self.assertEqual(self.udos.particleById(3).deltaV(), 50.0)
        self.udos.tick(100)
        self.udos.tick(100)
        self.assertEqual(self.udos.particleById(3).deltaV(), 0.0)
        self.assertTrue(3 in self.udos.nodeById(8).particles)