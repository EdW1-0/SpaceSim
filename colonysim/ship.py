from utility.vessel import Vessel

import enum


class ShipStatus(enum.StrEnum):
    CONSTRUCTION = "CONSTRUCTION"
    IDLE = "IDLE"
    ACTIVE = "ACTIVE"

class ShipStatusError(Exception):
    pass


class Ship(Vessel):
    def __init__(self, id, name, shipClass, locale=None, deltaV=0, cargo=None, status=ShipStatus.CONSTRUCTION, constructionProgress=0):
        super().__init__(cargo)
        self.id = id
        self.name = name
        self.shipClass = shipClass
        self.locale = locale
        self.dv = deltaV
        self.status = status
        if self.status == ShipStatus.CONSTRUCTION:
            self.constructionProgress = constructionProgress
        else:
            self.constructionProgress = 100

        self.crew = set()

    def deltaV(self):
        return self.dv

    def burnDeltaV(self, deltaV):
        self.dv -= deltaV

    def construct(self):
        if self.status != ShipStatus.CONSTRUCTION:
            raise ShipStatusError
        self.status = ShipStatus.IDLE

    def active(self):
        if self.status != ShipStatus.IDLE:
            raise ShipStatusError
        self.status = ShipStatus.ACTIVE

    def idle(self):
        if self.status != ShipStatus.ACTIVE:
            raise ShipStatusError
        self.status = ShipStatus.IDLE