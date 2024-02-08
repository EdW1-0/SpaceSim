import unittest

from colonysim import ShipClass


class TestShipClass(unittest.TestCase):
    def testShipClass(self):
        self.assertTrue(ShipClass)

    def testShipClassConstructor(self):
        self.assertTrue(ShipClass("LIFTER", "Lifter"))
        self.assertTrue(ShipClass("LIFTER", "Lifter", maxDeltaV=1000))
        self.assertTrue(ShipClass("LIFTER", "Lifter", maxDeltaV=1000, constructionTime=100, constructionCost={"AL": 100}))


    def testShipClassAttributes(self):
        sc = ShipClass("LIFTER", "Lifter")
        self.assertTrue(hasattr(sc, "name"))
        self.assertTrue(hasattr(sc, "id"))
        self.assertTrue(hasattr(sc, "maxDeltaV"))
        self.assertTrue(hasattr(sc, "baseConstructionCost"))
        self.assertTrue(hasattr(sc, "baseConstructionTime"))

class TestShipClassParameters(unittest.TestCase):
    def setUp(self):
        self.sc = ShipClass("LIFTER", "Lifter", maxDeltaV=1000, constructionCost={"AL": 10}, constructionTime=100)

    def testShipClassConstructionParams(self):
        self.assertEqual(self.sc.constructionTime(), 100)
        self.assertEqual(self.sc.constructionCost(), {"AL": 10})
        
