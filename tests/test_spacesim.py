import unittest

import spacesim as spacesim


class TestSpaceSim(unittest.TestCase):
    def testSpaceSim(self):
        self.assertTrue(spacesim)
        self.assertTrue(spacesim.main)
        self.assertTrue(spacesim.pygame)

    def testSpaceSimMain(self):
        self.assertFalse(spacesim.pygame.get_init())


#        spacesim.main()
#        self.assertTrue(spacesim.pygame.get_init())
