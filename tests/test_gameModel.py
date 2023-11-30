from gameModel import GameModel

import unittest

import os
import tempfile


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


class TestGameModelNewGame(unittest.TestCase):
    def setUp(self):
        self.gm = GameModel()

    def testGameModelLoad(self):
        self.gm.load()
        self.assertTrue(self.gm.get_init())

    def testGameModelFileNotFound(self):
        with self.assertRaises(FileNotFoundError):
            self.gm.load("not_a_json_path")

class TestGameModelLoadSave(unittest.TestCase):
    def setUp(self):
        self.gm = GameModel()
        self.file = tempfile.NamedTemporaryFile()


    def testGameModelFileSaveLoad(self):
        self.assertTrue(os.path.exists(self.file.name))
        self.assertEqual(os.path.getsize(self.file.name), 0)
        self.gm.load()
        for i in range(17):
            self.gm.timingMaster.step()
            self.gm.tick()

        self.assertEqual(self.gm.timingMaster.timestamp, 17)
        
        self.gm.saveModel(self.file)

        self.assertTrue(os.path.exists(self.file.name))
        self.assertGreater(os.path.getsize(self.file.name), 0)
        self.file.seek(0)

        newModel = GameModel()
        self.assertFalse(newModel.init)
        newModel.loadModel(self.file)
        self.assertTrue(newModel.init)
        self.assertEqual(newModel.timingMaster.timestamp, 17)

    def tearDown(self):
        self.file.close()

class TestGameModelValidateModel(unittest.TestCase):
    def setUp(self):
        self.gm = GameModel()

    def testGameModelValidate(self):
        self.assertFalse(self.gm.validateModel())

        self.gm.load()

        self.assertTrue(self.gm.validateModel())
