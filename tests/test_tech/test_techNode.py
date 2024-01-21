import unittest

import techtree.techNode as techNode
import techtree.techTree as techTree
from techtree.techEffect import TechEffect, TechEffectUnlock, TechEffectParameter



class TestTechNode(unittest.TestCase):
    def test_techNodeImport(self):
        self.assertNotEqual(techNode, False)
        self.assertNotEqual(techNode.TechNode, False)

    def test_techNodeInit(self):
        self.assertTrue(techNode.TechNode(0))
        self.assertTrue(techNode.TechNode(id=0))
        self.assertTrue(techNode.TechNode(id=0, name="Foo"))
        self.assertTrue(techNode.TechNode(id=0, name="Foo", description="Bar"))
        self.assertTrue(
            techNode.TechNode(id=0, name="Foo", description="Bar", cost=100)
        )
        self.assertTrue(
            techNode.TechNode(
                id=0, name="Foo", description="Bar", cost=100, ancestors=[3]
            )
        )
        self.assertTrue(
            techNode.TechNode(
                id=0,
                name="Foo",
                description="Bar",
                cost=100,
                ancestors=[3],
                effects=[{"class": "UNLOCK", "domain": "VEHICLE", "id": 3}],
            )
        )

    def test_techNodeBadEffects(self):
        with self.assertRaises(KeyError):
            techNode.TechNode(id=0, effects=[{"value": 0}])
        with self.assertRaises(KeyError):
            techNode.TechNode(id=0, effects=[{"effect": "BUILDING"}])
        with self.assertRaises(KeyError):
            techNode.TechNode(id=0, effects=[{"effect": "BYILDING", "value": 0}])
        with self.assertRaises(KeyError):
            techNode.TechNode(id=0, effects=[{"effect": 0, "value": 0}])

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
        self.assertEqual(
            self.nodeZero.description,
            "Basic singe-staged rockets allow for sub-orbital space flight",
        )
        self.assertEqual(self.nodeZero.ancestors, [])
        self.assertEqual(self.nodeZero.effects[0], TechEffectUnlock(domain= "SHIP", id= "SATURNVI"))

    def test_techNodeEffects(self):
        node3 = self.techTree.nodeById(3)
        self.assertEqual(node3.id, 3)
        self.assertEqual(node3.ancestors, [1, 2])
        self.assertEqual(node3.effects[0], TechEffectUnlock(domain = "BUILDING", id= "HAB"))
         #self.assertEqual(node3.effects[1], TechEffectParameter(parameter="RAD_RESISTANCE", value=20))
        self.assertEqual(node3.effects[3], TechEffectParameter(parameter="MARTIAN_CONSTRUCTION_SPEED", amount=1))




if __name__ == "__main__":
    unittest.main()
