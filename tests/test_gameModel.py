from gameModel import GameModel

import unittest


class TestGameModelModule(unittest.TestCase):
    def testGameModel(self):
        self.assertTrue(GameModel)

    def testGameModelConstructor(self):
        self.assertTrue(GameModel())


class TestGameModelClass(unittest.TestCase):
    def setUp(self):
        self.gm = GameModel()

    def testGameModelAttributes(self):
        self.assertTrue(hasattr(self.gm, "techTree"))
        self.assertTrue(hasattr(self.gm, "orbitSim"))
        self.assertTrue(hasattr(self.gm, "planetSim"))
        self.assertTrue(hasattr(self.gm, "timingMaster"))

    def testGameModelUnloaded(self):
        self.assertIsNone(self.gm.techTree)
        self.assertIsNone(self.gm.orbitSim)
        self.assertIsNone(self.gm.planetSim)
        self.assertIsNone(self.gm.timingMaster)
        self.assertFalse(self.gm.get_init())


class TestGameModelLoading(unittest.TestCase):
    def setUp(self):
        self.gm = GameModel()

    def testGameModelLoad(self):
        self.gm.load()
        self.assertTrue(self.gm.get_init())

    def testGameModelFileNotFound(self):
        with self.assertRaises(FileNotFoundError):
            self.gm.load("not_a_json_path")
