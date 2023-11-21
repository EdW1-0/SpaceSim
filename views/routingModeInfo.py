from dataclasses import dataclass

from colonysim import Ship
from orbitsim import OrbitTrajectory
from planetsim import SurfacePoint

@dataclass
class RoutingModeInfo:
    start: object = None
    end: object = None
    ship: Ship = None
    trajectory: OrbitTrajectory = None
    surfaceCoordinates: SurfacePoint = None
