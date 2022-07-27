import unittest

from personmodel.personGenerator import PersonGenerator

class TestPersonGenerator(unittest.TestCase):
    def testPersonGenerator(self):
        self.assertTrue(PersonGenerator)
        self.assertTrue(PersonGenerator())