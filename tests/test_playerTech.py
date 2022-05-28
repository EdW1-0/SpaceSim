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
        self.assertEqual(self.pt.discovered, set())        

    def test_playerTechDiscoveredReadOnly(self):
        with self.assertRaises(AttributeError):
            self.pt.discovered = {4}

class TestPlayerTechActiveTech(unittest.TestCase):
    def setUp(self):
        tt = techTree.TechTree()
        self.pt = playerTech.PlayerTech(tt)

    def test_playerTechActiveTech(self):
        self.assertEqual(self.pt.activeTech, None)

    def test_playerTechSetActiveTech(self):
        self.pt.setActiveTech(0)
        self.assertEqual(self.pt.activeTech.id, 0)

class TestPlayerTechDiscoverTech(unittest.TestCase):
    def setUp(self):
        tt = techTree.TechTree()
        self.pt = playerTech.PlayerTech(tt)

    def test_playerTechDiscoverTech(self):
        self.pt.setActiveTech(0)
        self.pt._completeTech()
        self.assertEqual(self.pt.discovered, {0})
        self.assertEqual(self.pt.activeTech, None)

    def test_playerTechDiscoverException(self):
        with self.assertRaises(ValueError):
            self.pt._completeTech()

class TestPlayerTechProgressTech(unittest.TestCase):
    def setUp(self):
        tt = techTree.TechTree()
        self.pt = playerTech.PlayerTech(tt)

    def test_playerTechReadProgress(self):
        self.assertEqual(self.pt.progress, 0)
    
    def test_playerTechMakeProgress(self):
        self.pt.addResearch(50)
        self.assertEqual(self.pt.progress, 50)
        self.pt.addResearch(100)
        self.assertEqual(self.pt.progress, 150)

    def test_playerTechMakeFullProgress(self):
        self.pt.setActiveTech(1)
        self.pt.addResearch(50)
        self.assertEqual(self.pt.discovered, set())
        self.pt.addResearch(100)
        self.assertEqual(self.pt.discovered, {1})
        self.assertEqual(self.pt.activeTech, None)
        self.assertEqual(self.pt.progress, 0)

    def test_playerTechResetProgress(self):
        self.pt.setActiveTech(1)
        self.pt.addResearch(50)
        self.assertEqual(self.pt.progress, 50)
        self.pt.setActiveTech(0)
        self.assertEqual(self.pt.progress, 0)
        self.assertEqual(self.pt.discovered, set())

class test_playerTechAccessPossibleTargets(unittest.TestCase):
    def setUp(self):
        tt = techTree.TechTree()
        self.pt = playerTech.PlayerTech(tt)

    def test_playerTechAccessPossibleTargets(self):
        self.assertEqual(self.pt.possibleTargets, {0,1,2})
        self.pt.setActiveTech(1)
        self.pt.addResearch(1000)
        self.assertEqual(self.pt.possibleTargets, {0,2,4})


class test_playerTechEffects(unittest.TestCase):
    def setUp(self):
        tt = techTree.TechTree()
        self.pt = playerTech.PlayerTech(tt)

    def test_playerTechHasAllowedBuildings(self):
        self.assertTrue(hasattr(self.pt, "allowedBuildings"))

    def test_playerTechHasAllowedVehicles(self):
        self.assertTrue(hasattr(self.pt, "allowedVehicles"))

    def test_playerTechEffectsWork(self):
        self.pt.setActiveTech(3)
        self.pt.addResearch(500)
        self.assertEqual(self.pt.allowedBuildings, [7])
    

