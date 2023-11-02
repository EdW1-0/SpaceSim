from dataclasses import dataclass

from colonysim.ship import Ship
from orbitsim.orbitTrajectory import OrbitTrajectory
from planetsim.surfacePoint import SurfacePoint

@dataclass
class RoutingModeInfo:
    start: object = None
    end: object = None
    ship: Ship = None
    trajectory: OrbitTrajectory = None
    surfaceCoordinates: SurfacePoint = None
