from views.guiContext import GUIContext

import unittest

class ScreenMock:
    pass

class ModelMock:
    pass


class TestGUIContextModule(unittest.TestCase):
    def testGUIContext(self):
        self.assertTrue(GUIContext)

    def testGUIContextConstructor(self):
        self.assertTrue(GUIContext(screen = ScreenMock(), model = ModelMock(), manager=None))

    def testGUIContextAttributes(self):
        self.assertTrue(hasattr(GUIContext(ScreenMock(), ModelMock(), manager=None), "screen"))
        self.assertTrue(hasattr(GUIContext(ScreenMock(), ModelMock(), manager=None), "model"))

    def testGUIContextRun(self):
        with self.assertRaises(NotImplementedError):
            GUIContext(ScreenMock(), ModelMock(), manager=None).run()

