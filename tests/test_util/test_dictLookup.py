import unittest

from utility.dictLookup import getIntId


class TestGetIntId(unittest.TestCase):
    def setUp(self):
        self.d = {0: "foo", 1: "bar", 3: "baz", "FOUR": "bee", -2: "kay", 3.67: "lee"}

    def testGetIntId(self):
        self.assertTrue(getIntId)

    def testGetIntIdIdsPresent(self):
        self.assertEqual(getIntId(0, self.d), "foo")
        self.assertEqual(getIntId(1, self.d), "bar")
        self.assertEqual(getIntId(3, self.d), "baz")

    def testGetIntIdMissingId(self):
        with self.assertRaises(KeyError):
            getIntId(2, self.d)

    def testGetIntIdNonInteger(self):
        with self.assertRaises(TypeError):
            getIntId(3.67, self.d)

        with self.assertRaises(TypeError):
            getIntId("FOUR", self.d)

    def testGetIntIdNegative(self):
        with self.assertRaises(ValueError):
            getIntId(-2, self.d)
