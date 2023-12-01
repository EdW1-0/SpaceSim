import unittest

from views.techContext import TechContext

from views.guiContext import GUIContext

class TestTechContext(unittest.TestCase):
    def testTechContext(self):
        self.assertTrue(TechContext)

    def testTechContextClassHierarchy(self):
        self.assertTrue(TechContext(None, None, None))
        self.assertTrue(issubclass(TechContext, GUIContext))