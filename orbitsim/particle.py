class DeltaVError(Exception):
    def __init__(self, deltaV=0.0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.deltaV = deltaV


class Particle:
    def __init__(self, id, velocity=0, payload=None):
        self.id = id
        self.velocity = velocity
        self.payload = payload

    def deltaV(self):
        try:
            deltaV = self.payload.deltaV()
        except AttributeError:
            deltaV = 0.0

        return deltaV

    def burnDeltaV(self, deltaV):
        if self.payload:
            if self.payload.deltaV() >= deltaV:
                self.payload.burnDeltaV(deltaV)
            else:
                raise DeltaVError(deltaV=self.payload.deltaV())
        else:
            raise DeltaVError
