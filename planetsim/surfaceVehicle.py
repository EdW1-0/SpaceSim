from dataclasses import dataclass

from planetsim.surfaceObject import SurfaceObject

from planetsim.surfacePoint import SurfacePoint

@dataclass
class SurfaceVehicle(SurfaceObject):
    fuel: int = 0
    maxV: int = 0
    destination: SurfacePoint = None
    fuelPerM: float = 1.0

    def setDestination(self, destination):
        self.destination = destination