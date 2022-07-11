from planetsim.surfacePoint import SurfacePoint

class SurfaceObject:
    def __init__(self, id, content, point, fuel = 0, maxV = 0):
        self.id = id
        self.point = point
        self.content = content
        self.fuel = fuel
        self.maxV = maxV
        self.destination = None