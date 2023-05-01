from dataclasses import dataclass

from planetsim.surfaceObject import SurfaceObject

from planetsim.surfacePoint import SurfacePoint

@dataclass
class SurfaceBase(SurfaceObject):
    colonyId: str = None
