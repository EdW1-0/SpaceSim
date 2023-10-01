from dataclasses import dataclass

from planetsim.surfaceObject import SurfaceObject


@dataclass
class SurfaceBase(SurfaceObject):
    colonyId: str = None
