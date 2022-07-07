from planetsim.surfacePath import pathsIntersect, SurfacePath

class SurfaceRegion:
    def __init__(self, id, homePoint, borders):
        self.id = id
        self.borders = borders
        self.homePoint = homePoint

    def pointInRegion(self, point):
        path = SurfacePath(point, self.homePoint)
        # If path from point to home point crosses border an even number of times, point is in region.
        inRegion = True
        for border in self.borders:
            if pathsIntersect(path, border):
                inRegion = not inRegion

        return inRegion