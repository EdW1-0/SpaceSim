from views.guiContext import GUIContext

from planetsim.planetSurface import PlanetSurface
from planetsim.surfacePoint import SurfacePoint, dot
from planetsim.surfaceRegion import SurfaceRegion
from planetsim.surfacePath import SurfacePath

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


polygonScale = 0.9

# For debugging polygon code
patchwork = True

class SurfaceContext(GUIContext):
    def __init__(self, screen, model, manager, meridian = (0, 0)):
        super(SurfaceContext, self).__init__(screen, model, manager)
        self.planet = PlanetSurface("json/planets/Mercury.json", radius = 1000)
        self.meridian = meridian
        #self.planet = PlanetSurface("test_json/test_surfaces/single_region_square.json", radius = 1000)
        #self.planet = PlanetSurface("test_json/test_surfaces/four_squares.json", radius = 1000)
        self.polyCount = 0

        self.surf = pygame.Surface((1200, 800))
        

        self.extractPolygons()
        print(self.polyCount)
        self.triangularise()
        print(self.polyCount)

        self.polygonise(polygonScale)
        print(self.polyCount)

        self.renderGlobe()

    ###TODO: Copy/pasted from SurfacePoint. Should pull both instances into a shared utility function
    def vector(self, latitude, longitude):
        latr = latitude / 180 * math.pi
        longr = longitude / 180 * math.pi
        x = math.cos(latr)*math.cos(longr)
        y = math.cos(latr)*math.sin(longr)
        z = math.sin(latr)
        return (x, y, z)
    
    def latLong(self, v):
        lat = math.atan2(v[2], math.sqrt(v[0]**2 + v[1]**2))
        long = math.atan2(v[1], v[0])
        return (lat*180.0/math.pi, long*180.0/math.pi)
    
    def vsum(self, v1, v2):
        assert(len(v1) == len(v2))
        v = tuple(v1[i] + v2[i] for i in range(len(v1)))
        return v
    
    def zRot(self, v, angle):
        phi = math.radians(angle)
        vx = v[0]*math.cos(phi) - v[1]*math.sin(phi)
        vy = v[0]*math.sin(phi) + v[1]*math.cos(phi)
        vz = v[2]
        return (vx, vy, vz)
    
    def yRot(self, v, angle):
        phi = math.radians(angle)
        vx = v[0]*math.cos(phi) + v[2]*math.sin(phi)
        vy = v[1]
        vz = -v[0]*math.sin(phi) + v[2]*math.cos(phi)
        return (vx, vy, vz)
    
    def xRot(self, v, angle):
        phi = math.radians(angle)
        vx = v[0]
        vy = v[1]*math.cos(phi) - v[2]*math.sin(phi)
        vz = v[1]*math.sin(phi) + v[2]*math.cos(phi)
        
        return (vx, vy, vz)
    



    def renderGlobe(self):
        self.surf.fill((50, 50, 50))

        print("Total: ", self.polyCount)
        drawCount = 0
        hideCount = 0
        for r in self.polygons.values():
            colour = (random.random()*255, random.random()*255, random.random()*255)
            for polygon in r:
                vectors = tuple(self.vector(v[0], v[1]) for v in polygon)
                v12 = self.vsum(vectors[0], vectors[1])
                v123 = self.vsum(v12, vectors[2])

                meridianV = self.vector(self.meridian[0], -self.meridian[1])
                if (dot(meridianV, v123) <= 0):
                    hideCount += 1
                    continue

                drawCount += 1
                if patchwork:
                    colour = (random.random()*255, random.random()*255, random.random()*255)
                coordinates = []
                for vertex in vectors:  
                    # Rotate vertex into coordinate system of meridian
                    
                    # if rx > 90.0:
                    #     delta = rx - 90.0
                    #     rx -= 2*delta
                    r = self.zRot(vertex, self.meridian[1])
                    r2 = self.yRot(r, self.meridian[0])
                    rotatedVertex = self.latLong(r2)
                    print(rotatedVertex)

                    screenVertex = self.latLongToXY(rotatedVertex)
                    coordinates.append(screenVertex)

                pygame.draw.polygon(self.surf, colour, coordinates)

        print("Total drawn:", drawCount)
        print("Total hidden:", hideCount)
        print(self.meridian)

    def extractPolygons(self):
        self.polygons = {}
        for r in self.planet.regions.values():
            loop = tuple((path.p1.latitude, path.p1.longitude) for path in r.borders)
            self.polygons[r.id] = [loop]
            self.polyCount+=1

    def triangularise(self):
        for loopSet in self.polygons.values():
            quads = True
            while quads:
                quads = False
                dropList = []
                for loop in loopSet:
                    if len(loop) > 3:
                        dropList.append(loop)
                        loopSet.append(loop[:3])
                        loopSet.append(loop[2:] + loop[:1])
                        self.polyCount +=1
                        quads = True
                for loop in dropList:
                    loopSet.remove(loop)
            
    def polygonise(self, scale):
        for loopSet in self.polygons.values():
            bigPolygons = True
            while bigPolygons:
                bigPolygons = False
                dropList = []
                addList = []
                for loop in loopSet:
                    for i in range(len(loop)):
                        if i == 0:
                            p1, p2, p3 = loop[0], loop[2], loop[1]
                        elif i == 1:
                            p1, p2, p3 = loop[1], loop[2], loop[0]
                        else:
                            p1, p2, p3 = loop[2], loop[0], loop[1]

                        sp12 = SurfacePath(SurfacePoint(p1[0], p1[1]), SurfacePoint(p2[0], p2[1]))
                        angle12 = sp12.gcAngle()
                        sp23 = SurfacePath(SurfacePoint(p2[0], p2[1]), SurfacePoint(p3[0], p3[1]))
                        angle23 = sp23.gcAngle()
                        sp31 = SurfacePath(SurfacePoint(p3[0], p3[1]), SurfacePoint(p1[0], p1[1]))
                        angle31 = sp31.gcAngle()
                        if angle12 >= angle23 and angle12 >= angle31:
                            sp = sp12
                            angle = angle12
                            (pi, pj, pk) = (p1, p2, p3)
                        elif angle23 >= angle12 and angle23 >= angle31:
                            sp = sp23
                            angle = angle23
                            (pi, pj, pk) = (p2, p3, p1)
                        elif angle31 >= angle12 and angle31 >= angle23:
                            sp = sp31
                            angle = angle31
                            (pi, pj, pk) = (p3, p1, p2)
                        else:
                            assert("Should never reach here!")
                            
                        if angle > scale:                            
                            bigPolygons = True
                            midpoint = sp.intermediatePoint(0.5)
                            dropList.append(loop)
                            # Two triangles to make:
                            # One from p1 - midpoint - (other)
                            # One from midpoint - p2 - (other)
                            pm = (midpoint.latitude, midpoint.longitude)
                            t1 = (pi, pm, pk)
                            t2 = (pm, pj, pk)
                            #print("Splitting", p1, p2, p3, "into", t1, "and" , t2)
                            addList.append(t1)
                            addList.append(t2)
                            self.polyCount += 2
                            if self.polyCount % 100 == 0:
                                print (self.polyCount)
                            break
                for loop in dropList:
                    if loop in loopSet:
                        loopSet.remove(loop)
                        self.polyCount -= 1
                    else:
                        print ("Already removed ", loop)

                loopSet += addList
                if self.polyCount > 100000:
                    return





            


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
        

    def meridianLatitude(self, delta):
        lat = self.meridian[0]
        lat += delta
        if lat > 90.0:
            lat = 90.0
        elif lat < -90.0:
            lat = -90.0

        self.meridian = (lat, self.meridian[1])

        print (self.meridian)

    def meridianLongitude(self, delta):
        long = self.meridian[1]
        long += delta
        long = long % 360.0
        self.meridian = (self.meridian[0], long)

        print (self.meridian)

        #lat = max(min(lat+delta, 90.0), -90.0)

    def run(self):
        returnCode = 0

        for event in pygame.event.get():
            if event.type == QUIT:
                returnCode = QUIT
                break
            elif event.type == MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                print (self.xyToLatLong(pos))
            elif event.type == KEYDOWN:
                if event.key == K_DOWN:
                    self.meridianLatitude(-20.0)
                    self.renderGlobe()
                elif event.key == K_UP:
                    self.meridianLatitude(20.0)
                    self.renderGlobe()
                elif event.key == K_RIGHT:
                    self.meridianLongitude(20.0)
                    self.renderGlobe()
                elif event.key == K_LEFT:
                    self.meridianLongitude(-20.0)
                    self.renderGlobe()






        self.screen.blit(self.surf, pygame.Rect(0, 0, 1200, 800))
        

        return returnCode