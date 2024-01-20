import unittest

from utility import loadEntityFile


class TestLoadEntityFile(unittest.TestCase):
    def testLoadEntityFile(self):
        self.assertTrue(loadEntityFile)

    def testLoadEntityFileBasic(self):
        class BasicMock:
            def __init__(self, id: str, data: int):
                self.id = id
                self.data = data

        basic = loadEntityFile(path="test_json/test_fileLoad", id="Basic", EntityClass=BasicMock)
        self.assertTrue(basic)
        self.assertEqual(len(basic), 3)
        self.assertEqual(basic["A"].id, "A")
        self.assertEqual(basic["A"].data, 1)

    def testLoadEntityFileAltClasS(self):
        class NormMock:
            def __init__(self, id: str, data: int):
                self.id = id
                self.data = data

        class AltMock(NormMock):
            def __init__(self, *args, altie, **kwargs):
                super(AltMock, self).__init__(*args, **kwargs)
                self.altie = altie

        alt = loadEntityFile(path="test_json/test_fileLoad", id="AltClass", EntityClass=NormMock, altClasses={"altie": AltMock})
        self.assertTrue(alt)
        self.assertTrue(isinstance(alt["NORMAL"], NormMock))
        self.assertTrue(isinstance(alt["ALT"], AltMock))
        self.assertEqual(alt["ALT"].altie["Q"], 7)