import unittest

import techTree

class TestTechTree(unittest.TestCase):
    
    def test_techTreeImport(self):
        self.assertNotEqual(techTree, False)
        self.assertNotEqual(techTree.TechTree, False)

    def test_techTreeInitialise(self):
        self.assertTrue(self.techTree)

    def setUp(self):
        self.techTree = techTree.TechTree()

    def test_techTreeAccessTree(self):
        self.assertTrue(self.techTree.tree)




if __name__ == '__main__':
    unittest.main()