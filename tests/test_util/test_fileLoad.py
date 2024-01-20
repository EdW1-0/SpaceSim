import unittest

from utility import loadEntityFile

class BasicMock:
    def __init__(self, id: str, data: int):
        self.id = id
        self.data = data

class TestLoadEntityFile(unittest.TestCase):
    def testLoadEntityFile(self):
        self.assertTrue(loadEntityFile)

    def testLoadEntityFileBasic(self):
        basic = loadEntityFile(path="test_json/test_fileLoad", id="Basic", EntityClass=BasicMock)
        self.assertTrue(basic)
        self.assertEqual(len(basic), 3)
        self.assertEqual(basic["A"].id, "A")
        self.assertEqual(basic["A"].data, 1)
