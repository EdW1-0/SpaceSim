class Ship:
    def __init__(self, id, name, shipClass, locale = None, deltaV=0, cargo = None):
        self.id = id
        self.name = name
        self.shipClass = shipClass
        self.locale = locale
        self.dv = deltaV
        if cargo is None:
            self.cargo = {}
        else:
            self.cargo = cargo

    def deltaV(self):
        return self.dv
    
    def burnDeltaV(self, deltaV):
        self.dv -= deltaV

    def addCargo(self, cargo):
        overage = {}
        for commodity in cargo:
            if commodity in self.cargo:
                self.cargo[commodity] += cargo[commodity]
                overage[commodity] = 0
            else:
                if cargo[commodity] > 0:
                    self.cargo[commodity] = cargo[commodity]
                overage[commodity] = 0
        return overage

    def removeCargo(self, cargo):
        retDict = {}
        for commodity in cargo:
            if commodity in self.cargo:
                if cargo[commodity] <= self.cargo[commodity]:
                    self.cargo[commodity] -= cargo[commodity]
                    retDict[commodity] = cargo[commodity]
                else:
                    retDict[commodity] = self.cargo[commodity]
                    del self.cargo[commodity]
            else:
                retDict[commodity] = 0

        return retDict
