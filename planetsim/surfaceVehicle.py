from dataclasses import dataclass

from planetsim.surfaceObject import SurfaceObject

from planetsim.surfacePoint import SurfacePoint

from planetsim.vehicle import Vehicle

@dataclass
class SurfaceVehicle(SurfaceObject):
    payload: Vehicle = None
    destination: SurfacePoint = None

    def setDestination(self, destination):
        self.destination = destination

    def fuel(self):
        return self.payload.fuel
    
    def maxV(self):
        return self.payload.maxV()
    
    def fuelPerM(self):
        return self.payload.fuelPerM()
    

    