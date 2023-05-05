import unittest

from colonysim.colonySim import ColonySim

class TestColonySim(unittest.TestCase):
    def testColonySim(self):
        self.assertTrue(ColonySim)

    def testColonySimConstructor(self):
        self.assertTrue(ColonySim())
        self.assertTrue(ColonySim(resourcePath = "json/resources"))
        self.assertTrue(ColonySim(reactionPath = "json/reactions"))
        self.assertTrue(ColonySim(buildingPath = "json/buildingClasses"))

    def testColonySimAttributes(self):
        cs = ColonySim()
        self.assertTrue(hasattr(cs, "_buildingClasses"))
        self.assertTrue(hasattr(cs, "_resources"))
        self.assertTrue(hasattr(cs, "_reactions"))
        self.assertTrue(hasattr(cs, "_colonies"))
        self.assertTrue(isinstance(cs._buildingClasses, dict))
        self.assertTrue(isinstance(cs._resources, dict))
        self.assertTrue(isinstance(cs._reactions, dict))
        self.assertTrue(isinstance(cs._colonies, dict))

    def testColonySimLoading(self):
        cs = ColonySim()
        self.assertTrue(len(cs._resources.values()) > 0)
        self.assertTrue(len(cs._reactions.values()) > 0)
        self.assertTrue(len(cs._buildingClasses.values()) > 0)

        csr = ColonySim(resourcePath="test_json/test_colony/test_resources")
        self.assertEqual(len(csr._resources.values()), 2)
        