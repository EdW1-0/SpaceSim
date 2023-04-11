class Ship:
    def __init__(self, name, deltaV=0):
        self.name = name
        self.dv = deltaV

    def deltaV(self):
        return self.dv
    
    def burnDeltaV(self, deltaV):
        self.dv -= deltaV