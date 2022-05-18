import unittest

import techNode

class TestTechNode(unittest.TestCase):
    def test_techNodeImport(self):
        self.assertNotEqual(techNode, False)
        self.assertNotEqual(techNode.TechNode, False)

    def test_techNodeInit(self):
        self.assertTrue(techNode.TechNode(0))

    def test_techNodeId(self):
        self.assertEqual(techNode.TechNode(0).id, 0)
        self.assertEqual(techNode.TechNode(1).id, 1)

if __name__ == '__main__':
    unittest.main()