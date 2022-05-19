import unittest

import techTree
import techNode

class TestTechTreeLoading(unittest.TestCase):
    
    def test_techTreeImport(self):
        self.assertNotEqual(techTree, False)
        self.assertNotEqual(techTree.TechTree, False)

    def test_techTreeInitialise(self):
        self.assertTrue(techTree.TechTree("json/Technologies.json"))
        with self.assertRaises(FileNotFoundError):
            techTree.TechTree("")
        self.assertTrue(techTree.TechTree())




class TestTechTreeInteraction(unittest.TestCase):

    def setUp(self):
        self.techTree = techTree.TechTree("json/Technologies.json")
        

    def test_techTreeAccessBadNode(self):
        with self.assertRaises(ValueError):
            self.techTree.nodeById(-1)
        with self.assertRaises(TypeError):
            self.techTree.nodeById("Foo")

    def test_techTreeAccessNode(self):
        self.assertNotEqual(self.techTree.nodeById(0), None)
        self.assertTrue(isinstance(self.techTree.nodeById(0), techNode.TechNode))
        self.assertEqual(self.techTree.nodeById(0), self.techTree.nodeById(0))
        self.assertNotEqual(self.techTree.nodeById(0), self.techTree.nodeById(1))

    def test_techTreeAccessNodeId(self):
        self.assertEqual(self.techTree.nodeById(0).id, 0)
        self.assertEqual(self.techTree.nodeById(1).id, 1)

    def test_techTreeTotalNodes(self):
        self.assertNotEqual(self.techTree.totalNodes, 0)
        self.assertEqual(self.techTree.totalNodes, 7)




if __name__ == '__main__':
    unittest.main()