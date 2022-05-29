import unittest

import techtree.techNode as techNode
import techtree.techTree as techTree
from techtree.techNode import TechEffect, TechEffectClass

from dataclasses import is_dataclass, FrozenInstanceError
from enum import Enum


class TestTechNode(unittest.TestCase):
    def test_techNodeImport(self):
        self.assertNotEqual(techNode, False)
        self.assertNotEqual(techNode.TechNode, False)

    def test_techNodeInit(self):
        self.assertTrue(techNode.TechNode(0))
        self.assertTrue(techNode.TechNode(id = 0))
        self.assertTrue(techNode.TechNode(id = 0, name = "Foo"))
        self.assertTrue(techNode.TechNode(id = 0, name = "Foo", description = "Bar"))
        self.assertTrue(techNode.TechNode(id = 0, name = "Foo", description = "Bar", cost = 100))
        self.assertTrue(techNode.TechNode(id = 0, name = "Foo", description = "Bar", cost = 100, ancestors = [3]))
        self.assertTrue(techNode.TechNode(id = 0, name = "Foo", description = "Bar", cost = 100, ancestors = [3], effects = [{"effect": "VEHICLE", "value": 3}]))

    def test_techNodeBadEffects(self):
        with self.assertRaises(KeyError):
            techNode.TechNode(id = 0, effects = [{"value": 0}])
        with self.assertRaises(KeyError):
            techNode.TechNode(id = 0, effects = [{"effect": "BUILDING"}])
        with self.assertRaises(KeyError):
            techNode.TechNode(id = 0, effects = [{"effect": "BYILDING", "value": 0}])
        with self.assertRaises(KeyError):
            techNode.TechNode(id = 0, effects = [{"effect": 0, "value": 0}])

    def test_techNodeId(self):
        self.assertEqual(techNode.TechNode(0).id, 0)
        self.assertEqual(techNode.TechNode(1).id, 1)


class TestTechNodeData(unittest.TestCase):
    def setUp(self):
        self.techTree = techTree.TechTree()
        self.nodeZero = self.techTree.nodeById(0)


    def test_techNodeAttributes(self):
        self.assertTrue(hasattr(self.nodeZero, "id"))
        self.assertTrue(hasattr(self.nodeZero, "name"))
        self.assertTrue(hasattr(self.nodeZero, "description"))
        self.assertTrue(hasattr(self.nodeZero, "cost"))
        self.assertTrue(hasattr(self.nodeZero, "ancestors"))
        self.assertTrue(hasattr(self.nodeZero, "effects"))

    def test_techNodeValues(self):
        self.assertEqual(self.nodeZero.id, 0)
        self.assertEqual(self.nodeZero.name, "Solid Fueled Rockets")
        self.assertEqual(self.nodeZero.cost, 50)
        self.assertEqual(self.nodeZero.description, "Basic singe-staged rockets allow for sub-orbital space flight")
        self.assertEqual(self.nodeZero.ancestors, [])
        self.assertEqual(self.nodeZero.effects, [])

    def test_techNodeEffects(self):
        node3 = self.techTree.nodeById(3)
        self.assertEqual(node3.id, 3)
        self.assertEqual(node3.ancestors, [1,2])
        self.assertEqual(node3.effects[0], TechEffect(TechEffectClass.BUILDING, 7))
        self.assertEqual(node3.effects[1], TechEffect(TechEffectClass.VEHICLE, 3))

class TestTechEffect(unittest.TestCase):
    def test_techEffectLoad(self):
        self.assertNotEqual(techNode.TechEffect, False)
        self.assertTrue(is_dataclass(techNode.TechEffect))

    def test_techEffectInit(self):
        self.assertTrue(techNode.TechEffect(0, 0))

    def test_techEffectAttributes(self):
        self.assertTrue(hasattr(techNode.TechEffect(0, 0), "effect"))
        self.assertTrue(hasattr(techNode.TechEffect(0, 0), "value"))
        self.assertTrue(isinstance(techNode.TechEffect(techNode.TechEffectClass.BUILDING, 0).effect, techNode.TechEffectClass))

    def test_techEffectEquality(self):
        self.assertEqual(techNode.TechEffect(0,0), techNode.TechEffect(0,0))
        self.assertNotEqual(techNode.TechEffect(1,1), techNode.TechEffect(0,0))

    def test_techEffectImmutable(self):
        with self.assertRaises(FrozenInstanceError):
            techNode.TechEffect(0,0).effect = 0
        with self.assertRaises(FrozenInstanceError):
            techNode.TechEffect(1,1).value = 3

class TestTechEffectClass(unittest.TestCase):
        def test_techEffectClassInit(self):
            self.assertNotEqual(techNode.TechEffectClass, False)
            self.assertTrue(techNode.TechEffectClass(0))

        def test_techEffectClassIntrospection(self):
            self.assertTrue(issubclass(techNode.TechEffectClass, Enum))
            self.assertTrue(isinstance(techNode.TechEffectClass.BUILDING, techNode.TechEffectClass))
            self.assertTrue(isinstance(techNode.TechEffectClass(1), techNode.TechEffectClass))



if __name__ == '__main__':
    unittest.main()