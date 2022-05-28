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
        with self.assertRaises(KeyError):
            self.techTree.nodeById(99)

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

    def test_techTreeNodeGap(self):
        tt = techTree.TechTree("test_json/test_id_gap.json")
        self.assertEqual(tt.nodeById(5).id, 5)

    def test_techTreeNodeReverseOrder(self):
        tt = techTree.TechTree("test_json/test_id_out_of_order.json")
        self.assertEqual(tt.nodeById(3).id, 3)
        self.assertEqual(tt.nodeById(4).id, 4)
        self.assertEqual(tt.nodeById(5).id, 5)

class TestTechTreeValidation(unittest.TestCase):
    def test_techTreeRejectDuplicates(self):
        with self.assertRaises(AssertionError):
            techTree.TechTree("test_json/test_duplicates.json")


    def test_techTreeRejectLoops(self):
        with self.assertRaises(AssertionError):
            techTree.TechTree("test_json/test_loops_unary.json")
        with self.assertRaises(AssertionError):
            techTree.TechTree("test_json/test_loops_binary.json")
        with self.assertRaises(AssertionError):
            techTree.TechTree("test_json/test_loops_ternary.json")


    def test_techTreeNonExistantAncestor(self):
        with self.assertRaises(AssertionError):
            techTree.TechTree("test_json/test_invalid_ancestor.json")

class TestTechTreeLinkage(unittest.TestCase):
    def setUp(self):
        self.techTree = techTree.TechTree("test_json/test_happy_case.json")

    def test_techTreeAncestorLookup(self):
        self.assertEqual([node.id for node in self.techTree.ancestorsOfId(5)], [3,4])
        self.assertEqual(self.techTree.ancestorsOfId(0), [])
        self.assertEqual([node.id for node in self.techTree.ancestorsOfId(self.techTree.ancestorsOfId(5)[0].id)], [1,2])

        

    def test_techTreeDescendentLookup(self):
        self.assertEqual([node.id for node in self.techTree.descendentsOfId(1)], [3,4])
        self.assertEqual(self.techTree.descendentsOfId(0), [])






if __name__ == '__main__':
    unittest.main()