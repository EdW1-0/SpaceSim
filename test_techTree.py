import unittest

import techTree

class TestTechTree(unittest.TestCase):
    
    def test_techTreeImport(self):
        self.assertNotEqual(techTree, False)
        self.assertNotEqual(techTree.TechTree, False)





if __name__ == '__main__':
    unittest.main()