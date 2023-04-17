from views.guiContext import GUIContext

from planetsim.planetSurface import PlanetSurface
from planetsim.surfacePoint import SurfacePoint
from planetsim.surfaceRegion import SurfaceRegion

import pygame
import math, random

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    MOUSEBUTTONUP,
    QUIT,
)

LOADSURFACEVIEW = pygame.USEREVENT + 3


center = (500, 400)
radius = 300.0

class SurfaceContext(GUIContext):
    def __init__(self, screen, model, manager):
        super(SurfaceContext, self).__init__(screen, model, manager)
        self.planet = PlanetSurface("json/planets/Mercury.json", radius = 1000)

        self.surf = pygame.Surface((1200, 800))
        self.surf.fill((50, 50, 50))

        self.extractPolygons()

        for r in self.polygons.values():

            for polygon in r:
                colour = (random.random()*255, random.random()*255, random.random()*255)
                coordinates = []
                for vertex in polygon:
                    screenVertex = self.latLongToXY(vertex)
                    coordinates.append(screenVertex)

                pygame.draw.polygon(self.surf, colour, coordinates)
            # For each region
            # Decide if drawing
            # Find each vertex and covert to screen coordinates
            # Pick a random colour
            # Draw a polygon with those coordinates

    def extractPolygons(self):
        self.polygons = {}
        for r in self.planet.regions.values():
            if r.homePoint.longitude > 90.0 and r.homePoint.longitude < 270.0:
                continue

            loop = tuple((path.p1.latitude, path.p1.longitude) for path in r.borders)
            self.polygons[r.id] = [loop]

    def triangularise(self):
        for loopSet in self.polygons.values():
            noQuads = True
            while noQuads:
                noQuads = False
                for loop in loopSet:
                    if len(loop) > 3:
                        pass
            
            


        # pxArray = pygame.surfarray.pixels3d(self.surf)
        # shape = pxArray.shape
        # for i in range(shape[0]):
        #     for j in range(shape[1]):
        #         x = i - center[0]
        #         y = j - center[1]
        #         measure = (x*x + y*y)
        #         r = math.sqrt(measure)
        #         if r < 300:
        #             (lat, long) = self.xyToLatLong((x, y))
        #             sp = SurfacePoint(lat, long)
        #             for r in self.planet.regions.values():
        #                 if r.pointInRegion(sp):
        #                     if r.id % 2:
        #                         pxArray[i, j, 0] = 200
        #                         pxArray[i, j, 1] = 100
        #                         pxArray[i, j, 2] = 10
        #                     else:
        #                         pxArray[i, j, 0] = 10
        #                         pxArray[i, j, 1] = 200
        #                         pxArray[i, j, 2] = 100

  
        #         else:
        #             pxArray[i, j, 0] = 10
        #             pxArray[i, j, 1] = 10
        #             pxArray[i, j, 2] = 10

        # del pxArray

    def xyToLatLong(self, pos = center):
        (x, y) = (pos[0] - center[0], pos[1] - center[1])
        height = y/radius
        if abs(height) > 1.0:
            return (-999, -999)
        
        lat = -math.asin(height)

        width = x/radius/math.cos(lat) 
        if abs(width) > 1.0:
            return (999, 999)
        long = math.asin(width) 
        
        return (math.degrees(lat), math.degrees(long) % 360.0)
    
    def latLongToXY(self, pos = (0, 0)):
        (lat, long) = (math.radians(pos[0]), math.radians(pos[1]))
        height = math.sin(-lat)
        y = height * radius
        width = math.sin(long)
        x = width * radius * math.cos(lat)
        return (x + center[0], y + center[1])
        


    def run(self):
        returnCode = 0

        for event in pygame.event.get():
            if event.type == QUIT:
                returnCode = QUIT
                break
            elif event.type == MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                print (self.xyToLatLong(pos))





        self.screen.blit(self.surf, pygame.Rect(0, 0, 1200, 800))
        

        return returnCode