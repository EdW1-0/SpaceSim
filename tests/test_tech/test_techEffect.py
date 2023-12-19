import unittest
from techtree.techEffect import TechEffect, TechEffectUnlock, TechEffectParameter

from dataclasses import is_dataclass, FrozenInstanceError
from enum import Enum


class TestTechEffect(unittest.TestCase):
    def test_techEffectLoad(self):
        self.assertNotEqual(TechEffect, False)
        self.assertTrue(is_dataclass(TechEffect))

    def test_techEffectInit(self):
        self.assertTrue(TechEffect())

    def test_techEffectAttributes(self):
        self.assertTrue(hasattr(TechEffectUnlock("foo", 7), "domain"))
        self.assertTrue(hasattr(TechEffectUnlock("foo", 6), "id"))
        self.assertTrue(hasattr(TechEffectParameter("bar", 7), "parameter"))
        self.assertTrue(hasattr(TechEffectParameter("bar", 6), "amount"))



    def test_techEffectEquality(self):
        self.assertEqual(TechEffect(), TechEffect())
        self.assertNotEqual(TechEffectUnlock("foo", 3), TechEffect())

    def test_techEffectImmutable(self):
        with self.assertRaises(FrozenInstanceError):
            TechEffect().effect = 0
        with self.assertRaises(FrozenInstanceError):
            TechEffectUnlock("foo", 3).id = 7

    def test_techEffectStr(self):
        teu = TechEffectUnlock("foo", "bar")
        self.assertEqual(teu.__str__(), "Unlock {0} {1}".format("foo", "bar"))

        tep = TechEffectParameter("baz", 9)
        self.assertEqual(tep.__str__(), "Modify {0}: {1}".format("baz", 9))


