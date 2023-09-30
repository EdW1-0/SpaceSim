import unittest

from colonysim.resource import Resource


class TestResource(unittest.TestCase):
    def testResource(self):
        self.assertTrue(Resource)

    def testResourceConstructor(self):
        self.assertTrue(Resource("H2", "Hydrogen"))
        self.assertTrue(Resource("H2", "Hydrogen", baseValue=100.0))
        self.assertTrue(Resource("O2", "Oxygen", units="m^3"))

    def testResourceAttributes(self):
        r = Resource("STEEL", "Steel")
        self.assertTrue(hasattr(r, "id"))
        self.assertTrue(hasattr(r, "name"))
        self.assertTrue(hasattr(r, "baseValue"))
        self.assertTrue(hasattr(r, "units"))
