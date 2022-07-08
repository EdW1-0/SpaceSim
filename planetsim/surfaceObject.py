from planetsim.surfacePoint import SurfacePoint

class SurfaceObject:
    def __init__(self):
        self.point = SurfacePoint(0,0)
        self.content = None
        self.fuel = 0
        self.maxV = 0
        self.destination = None