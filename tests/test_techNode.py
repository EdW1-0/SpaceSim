import unittest

import techNode
import techTree

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
        self.assertTrue(techNode.TechNode(id = 0, name = "Foo", description = "Bar", cost = 100, ancestors = [3], effects = []))


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



if __name__ == '__main__':
    unittest.main()