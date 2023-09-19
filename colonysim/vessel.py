class Vessel:
    def __init__(self, cargo = None):
        if cargo is None:
            self.cargo = {}
        else:
            self.cargo = cargo

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