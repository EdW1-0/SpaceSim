from views.orbitContext import OrbitContext
from views.guiContext import GUIContext

import unittest
from tests.test_views.test_guiContext import ScreenMock, ModelMock

class TestOrbitContext(unittest.TestCase):
    def testOrbitContext(self):
        self.assertTrue(OrbitContext)