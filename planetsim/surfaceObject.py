from dataclasses import dataclass

from planetsim.surfacePoint import SurfacePoint

@dataclass
class SurfaceObject:
    id: int
    content: object
    point: SurfacePoint = None
    fuel: int = 0
    maxV: int = 0
    destination: SurfacePoint = None
    fuelPerM: float = 1.0

    def setDestination(self, destination):
        self.destination = destination