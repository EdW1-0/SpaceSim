import unittest

import playerTech
import techTree

class TestPlayerTechImport(unittest.TestCase):
    def test_playerTechImport(self):
        self.assertNotEqual(playerTech, False)
        self.assertNotEqual(playerTech.PlayerTech, False)

class TestPlayerTechConstructor(unittest.TestCase):
    def test_playerTechConstructor(self):
        self.assertTrue(playerTech.PlayerTech())
        self.assertTrue(playerTech.PlayerTech(techTree.TechTree()))
        

class TestPlayerTechDiscovered(unittest.TestCase):
    def setUp(self):
        self.pt = playerTech.PlayerTech()

    def test_playerTechDiscoveredEmpty(self):
        self.assertEqual(self.pt.discovered, [])        
