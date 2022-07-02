from dataclasses import dataclass

from planetsim.surfacePoint import SurfacePoint

# Encodes an arc on a great circle path as a pair of points. 
# By convention is the shortest GC path between them, unless long is set in which case it is the 
# reverse (long) path that is taken.
# For antipodes the choice of path is ambiguous. In this case we follow a convention:
# "Short" path is the path travelling east from p1.
# If path is on a meridian, then "short" path is northwards. 

@dataclass
class SurfacePath:
    p1: SurfacePoint = SurfacePoint(0,0)
    p2: SurfacePoint = SurfacePoint(0,0) 
    long: bool = False

        
