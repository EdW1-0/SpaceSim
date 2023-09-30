from dataclasses import dataclass

from planetsim.surfacePoint import SurfacePoint

# Inheritance hierarchy:
# - SurfaceObject:
#   - Location, id, name
#
# - Landmark
#   - class
#
# - Colony
#   - colony id, crew? Vehicles? Ships? Resources?
#
# - Vehicle
#   - Fuel, maxV, range, destination, crew, cargo, equipment?


@dataclass
class SurfaceObject:
    id: int
    content: object
    point: SurfacePoint = None
    name: str = "Default object"
    killed: bool = False

    def kill(self):
        self.killed = True
