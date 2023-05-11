from colonysim.reaction import Reaction

from enum import Enum

class OrderStatus(Enum):
    PENDING = 0,
    RUNNING = 1,
    PAUSED = 2


class ProductionOrder:
    def __init__(self, id, reaction, amount = 0):
        self.id = id
        self.amount = amount
        if not isinstance(reaction, Reaction):
            raise TypeError
        if amount < 0:
            raise ValueError
        self.reaction = reaction
        self.status = OrderStatus.PENDING

    def start(self):
        self.status = OrderStatus.RUNNING

    def pause(self):
        self.status = OrderStatus.PAUSED