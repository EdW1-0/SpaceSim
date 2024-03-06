import unittest
from unittest.mock import MagicMock

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

    def testLoadEntityFileAltClass(self):
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

    def testLoadEntityFileKwargs(self):
        class KwargMock:
            def __init__(self, id: str, data: int, volatileData: int, callback=None):
                self.id = id
                self.data = data 
                self.volatileData = volatileData
                self.callback = callback

            def call(self):
                self.callback()

            
        cb = MagicMock(return_value = 8)

        kway = loadEntityFile(path="test_json/test_fileLoad", id="KeywordTest", EntityClass=KwargMock, volatileData = 23, callback = cb)
        self.assertTrue(kway)
        self.assertEqual(kway["A"].id, "A")
        self.assertEqual(kway["A"].volatileData, 23)
        self.assertEqual(kway["A"].callback(), 8)
        cb.assert_called_once()

    def testLoadEntityFileAltSpecificArguments(self):
        class NormMock:
            def __init__(self, id: str, data: int):
                self.id = id
                self.data = data

        class AltMock(NormMock):
            def __init__(self, id: str, data: int, altArg: str, callback, bonusParam: str):
                super(AltMock, self).__init__(id, data)
                self.altArg = altArg
                self.callback = callback
                self.bonusParam = bonusParam

        cb = MagicMock(return_value = "Howdy")

        altArgs = loadEntityFile(path="test_json/test_fileLoad", 
                                 id="AltArgs", 
                                 EntityClass=NormMock, 
                                 altClasses={
                                     "altArg": (AltMock, {"callback": cb, "bonusParam": "Sparkly"})
                                 })
        self.assertTrue(altArgs)
        self.assertTrue(isinstance(altArgs["NORMAL"], NormMock))
        self.assertTrue(isinstance(altArgs["ALT"], AltMock))
        self.assertEqual(altArgs["ALT"].altArg, "spinach")
        self.assertEqual(altArgs["ALT"].bonusParam, "Sparkly")
        self.assertEqual(altArgs["ALT"].callback(), "Howdy")
        cb.assert_called_once()

    def testLoadEntityFileKwModifier(self):
        class KWMock:
            def __init__(self, id: str, data: int, kwData: int):
                self.id = id
                self.data = data 
                self.funnyData = kwData

        def modifier(modData, modClass):
            if modClass == "DOUBLE":
                return int(modData) * 2
            elif modClass == "HALF":
                return int(modData) / 2

        dictOutput = loadEntityFile(
            path="test_json/test_fileLoad", 
            id="ModifierTest", 
            EntityClass=KWMock, 
            modifiers = {"kwData": [modifier, "class"]})
        
        self.assertTrue(dictOutput)
        self.assertEqual(dictOutput[0].funnyData, 8)
        self.assertEqual(dictOutput[1].funnyData, 3)
        self.assertFalse(hasattr(dictOutput[0], "class"))
        self.assertFalse(hasattr(dictOutput[1], "class"))
