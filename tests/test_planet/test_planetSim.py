from planetsim import PlanetSim, VehicleClass, Vehicle

import unittest


class TestPlanetSim(unittest.TestCase):
    def testPlanetSimImport(self):
        self.assertTrue(PlanetSim)

    def testPlanetSimAttributes(self):
        self.assertTrue(hasattr(PlanetSim(None, "json/Planets.json"), "planets"))

    def testPlanetSimConstructor(self):
        with self.assertRaises(FileNotFoundError):
            PlanetSim(None, jsonPath="")
        self.assertTrue(PlanetSim(None, jsonPath="json/Planets.json"))
        self.assertNotEqual(
            len(PlanetSim(None, jsonPath="json/Planets.json").planets), 0
        )


class TestPlanetSimInteraction(unittest.TestCase):
    def setUp(self):
        self.planetSim = PlanetSim(None, "json/Planets.json")

    def test_planetSimAccessBadNode(self):
        with self.assertRaises(KeyError):
            self.planetSim.planetById(-1)
        with self.assertRaises(ValueError):
            self.planetSim.planetById("Foo")
        with self.assertRaises(KeyError):
            self.planetSim.planetById(99)

    def test_planetSimAccessNode(self):
        self.assertNotEqual(self.planetSim.planetById("MERCURY"), None)

class TestPlanetSimVehicles(unittest.TestCase):
    def setUp(self):
        self.planetSim = PlanetSim(None, "json/Planets.json")
        self.vc = VehicleClass(0, "Rover")

    def test_planetSimCreateVehicle(self):
        vehicle_id = self.planetSim.createVehicle("Rover 1", self.vc, fuel=100)
        self.assertIn(vehicle_id, self.planetSim.vehicles)
        self.assertIsInstance(self.planetSim.vehicles[vehicle_id], Vehicle)
        self.assertEqual(self.planetSim.vehicles[vehicle_id].name, "Rover 1")
        self.assertEqual(self.planetSim.vehicles[vehicle_id].fuel, 100)
