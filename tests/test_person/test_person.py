import unittest

from personmodel.person import Person

class TestPerson(unittest.TestCase):
    def testPerson(self):
        self.assertTrue(Person)
        self.assertTrue(Person())