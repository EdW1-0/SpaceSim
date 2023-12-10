import unittest
from techtree.techEffect import TechEffect, TechEffectClass

from dataclasses import is_dataclass, FrozenInstanceError
from enum import Enum


class TestTechEffect(unittest.TestCase):
    def test_techEffectLoad(self):
        self.assertNotEqual(TechEffect, False)
        self.assertTrue(is_dataclass(TechEffect))

    def test_techEffectInit(self):
        self.assertTrue(TechEffect(0, 0))

    def test_techEffectAttributes(self):
        self.assertTrue(hasattr(TechEffect(0, 0), "effect"))
        self.assertTrue(hasattr(TechEffect(0, 0), "value"))
        self.assertTrue(
            isinstance(
                TechEffect(TechEffectClass.BUILDING, 0).effect,
                TechEffectClass,
            )
        )

    def test_techEffectEquality(self):
        self.assertEqual(TechEffect(0, 0), TechEffect(0, 0))
        self.assertNotEqual(TechEffect(1, 1), TechEffect(0, 0))

    def test_techEffectImmutable(self):
        with self.assertRaises(FrozenInstanceError):
            TechEffect(0, 0).effect = 0
        with self.assertRaises(FrozenInstanceError):
            TechEffect(1, 1).value = 3


class TestTechEffectClass(unittest.TestCase):
    def test_techEffectClassInit(self):
        self.assertNotEqual(TechEffectClass, False)
        self.assertTrue(TechEffectClass(0))

    def test_techEffectClassIntrospection(self):
        self.assertTrue(issubclass(TechEffectClass, Enum))
        self.assertTrue(
            isinstance(TechEffectClass.BUILDING, TechEffectClass)
        )
        self.assertTrue(
            isinstance(TechEffectClass(1), TechEffectClass)
        )
