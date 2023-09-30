import unittest

from colonysim.reaction import Reaction


class TestReaction(unittest.TestCase):
    def testReaction(self):
        self.assertTrue(Reaction)

    def testReactionConstructor(self):
        self.assertTrue(Reaction("NULL", "Do nothing"))
        self.assertTrue(Reaction("PV", "Solar Power", outputs={"E": 100.0}))
        self.assertTrue(Reaction("SPOIL", "Food Spoilage", inputs={"FOOD": 1}))
        self.assertTrue(
            Reaction(
                "CO2H2O",
                "Sabatier Reaction",
                inputs={"CO2": 1, "H2O": 2},
                outputs={"CH4": 1, "O2": 2},
            )
        )

    def testReactionAttribute(self):
        r = Reaction("TEST", "Test Reaction")
        self.assertTrue(hasattr(r, "id"))
        self.assertTrue(hasattr(r, "name"))
        self.assertTrue(hasattr(r, "inputs"))
        self.assertTrue(hasattr(r, "outputs"))
        self.assertTrue(isinstance(r.inputs, dict))
        self.assertTrue(isinstance(r.outputs, dict))
