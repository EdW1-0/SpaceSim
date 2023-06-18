class Ship:
    def __init__(self, id, name, shipClass, locale = None, deltaV=0):
        self.id = id
        self.name = name
        self.shipClass = shipClass
        self.locale = locale
        self.dv = deltaV

    def deltaV(self):
        return self.dv
    
    def burnDeltaV(self, deltaV):
        self.dv -= deltaV