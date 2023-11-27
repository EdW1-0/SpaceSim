import unittest

from utility import IDGenerator

class TestIdGenerator(unittest.TestCase):
    def testIdGenerator(self):
        self.assertTrue(IDGenerator)
    
    def testIdGeneratorConstructor(self):
        self.assertTrue(IDGenerator())

    def testIdGeneratorNewId(self):
        gen = IDGenerator()

        newId = gen.generateId()
        self.assertEqual(newId, 0)
        self.assertEqual(gen.generateId(), 1)

        for i in range(10):
            self.assertEqual(gen.generateId(), i+2)

    def testIdGeneratorRememberState(self):
        gen = IDGenerator()
        for i in range(3):
            gen.generateId()

        gen.nextId = 0

        self.assertEqual(gen.generateId(), 3)

    def testIdGeneratorSetId(self):
        gen = IDGenerator()
        self.assertEqual(gen.setId(0), 0)
        self.assertEqual(gen.setId(3), 3)

    def testIdGeneratorSkipIds(self):
        gen = IDGenerator()
        gen.setId(0)
        gen.setId(2)
        self.assertEqual(gen.generateId(), 1)
        self.assertEqual(gen.generateId(), 3)

    def testIdGeneratorDuplicateIds(self):
        gen = IDGenerator()
        gen.generateId()
        gen.setId(1)
        with self.assertRaises(KeyError):
            gen.setId(0)
        with self.assertRaises(KeyError):
            gen.setId(1)

    def testIdGeneratorIds(self):
        gen = IDGenerator()
        gen.generateId()
        gen.setId(2)
        self.assertEqual(gen.ids, {0, 2})
        

    def testIdGeneratorClearIds(self):
        gen = IDGenerator()
        gen.generateId()
        gen.setId(3)
        gen.generateId()
        gen.clearId(0)
        gen.clearId(3)

        self.assertEqual(gen.ids, {1})

    def testIdGeneratorClearMissingIdException(self):
        gen = IDGenerator()
        with self.assertRaises(KeyError):
            gen.clearId(2)
        