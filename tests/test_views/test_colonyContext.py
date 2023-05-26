import unittest

from views.colonyContext import ColonyContext
from views.guiContext import GUIContext

class ModelMock:
    pass

class TestColonyContext(unittest.TestCase):
    def testColonyContext(self):
        self.assertTrue(ColonyContext)

    def testColonyContextConstructor(self):
        self.assertTrue(ColonyContext(ModelMock(), ModelMock(), None))

    def testColonyContextInheritance(self):
        cc = ColonyContext(ModelMock(), ModelMock(), None)
        self.assertTrue(issubclass(ColonyContext, GUIContext))
        self.assertTrue(isinstance(cc, GUIContext))
         