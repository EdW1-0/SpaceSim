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
        self.assertTrue(self.gm.techTree)
        self.assertTrue(self.gm.orbitSim)

