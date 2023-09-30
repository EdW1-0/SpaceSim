import unittest

from colonysim.productionOrder import ProductionOrder, OrderStatus
from colonysim.reaction import Reaction


class TestProductionOrder(unittest.TestCase):
    def setUp(self):
        self.r = Reaction(0, "MOCK", inputs={"Na": 1, "Cl": 1}, outputs={"NaCl": 1})

    def testProductionOrder(self):
        self.assertTrue(ProductionOrder)
        self.assertTrue(OrderStatus)

    def testProductionOrderConstructor(self):
        self.assertTrue(ProductionOrder(0, reaction=self.r, amount=10))
        with self.assertRaises(TypeError):
            ProductionOrder(0, "ELECTROLYSIS", 10)
        with self.assertRaises(ValueError):
            ProductionOrder(0, self.r, -1)

    def testProductionOrderAttributes(self):
        po = ProductionOrder(0, reaction=self.r, amount=10)
        self.assertTrue(hasattr(po, "id"))
        self.assertTrue(hasattr(po, "reaction"))
        self.assertTrue(hasattr(po, "amount"))
        self.assertTrue(hasattr(po, "remaining"))
        self.assertTrue(hasattr(po, "status"))

    def testProductionOrderStatus(self):
        po = ProductionOrder(0, self.r, 100)
        self.assertEqual(po.status, OrderStatus.PENDING)
        po.start()
        self.assertEqual(po.status, OrderStatus.RUNNING)
        po.pause()
        self.assertEqual(po.status, OrderStatus.PAUSED)
        po.start()
        self.assertEqual(po.status, OrderStatus.RUNNING)
