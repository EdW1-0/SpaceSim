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
        self.assertTrue(GUIContext(screen = ScreenMock(), model = ModelMock()))

    def testGUIContextAttributes(self):
        self.assertTrue(hasattr(GUIContext(ScreenMock(), ModelMock()), "screen"))
        self.assertTrue(hasattr(GUIContext(ScreenMock(), ModelMock()), "model"))

    def testGUIContextRun(self):
        with self.assertRaises(NotImplementedError):
            GUIContext(ScreenMock(), ModelMock()).run()

