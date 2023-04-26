from views.guiContext import GUIContext

from views.timingView import TimingPanel
from views.sidePanels.sideStatusPanel import PlanetStatusPanel

from planetsim.planetSurface import PlanetSurface
from planetsim.surfacePoint import SurfacePoint, dot, vector, latLong
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
    MOUSEWHEEL,
    QUIT,
)

from pygame_gui.elements import UIButton
from pygame_gui  import (
    UI_BUTTON_PRESSED,
    UI_SELECTION_LIST_NEW_SELECTION
)


LOADSURFACEVIEW = pygame.USEREVENT + 3


center = (500, 400)


polygonScale = 0.2

# For debugging polygon code
patchwork = False

class SurfaceObjectSprite(pygame.sprite.Sprite):
    def __init__(self, surfaceObject, center=(0, 0), selected = False):
        super(SurfaceObjectSprite, self).__init__()
        self.center = center
        self.surfaceObject = surfaceObject
        self.selected = selected
        self.update()
        self.surf = pygame.surface.Surface((22, 22))
        self.surf.set_colorkey((0, 0, 0))
        pygame.draw.circle(self.surf, (5, 250, 5), (11, 11), 10.0)
    
    def latLong(self):
        return (self.surfaceObject.point.latitude, self.surfaceObject.point.longitude)
    
    def update(self):
        self.surf = pygame.surface.Surface((22, 22))
        self.surf.set_colorkey((0, 0, 0))
        if self.selected:
            colour = (230, 230, 5)
        else:
            colour = (5, 250, 5)
        pygame.draw.circle(self.surf, colour, (11, 11), 10.0)
        self.rect = self.surf.get_rect(center = self.center)
        

class SurfaceContext(GUIContext):
    def __init__(self, screen, model, manager, planet, meridian = (0, 0), radius = 300.0):
        super(SurfaceContext, self).__init__(screen, model, manager)
        self.planet = planet
        self.meridian = meridian
        self.radius = radius
        #self.planet = PlanetSurface("test_json/test_surfaces/single_region_square.json", radius = 1000)
        #self.planet = PlanetSurface("test_json/test_surfaces/four_squares.json", radius = 1000)
        self.polyCount = 0
        self.surf = pygame.Surface((1200, 800))

        self.selectedObject = None

        if self.planet.surface:
            self.planetSurface = self.planet.surface
    
            self.regionColours = {}
            for r in self.planetSurface.regions.values():
                self.computeRegionColour(r)

            self.extractPolygons()
            print(self.polyCount)
            self.triangularise()
            print(self.polyCount)

            self.polygonise(polygonScale)
            print(self.polyCount)
        else:
            self.planetSurface = None

        self.renderGlobe()

        all_sprites = pygame.sprite.Group()
        object_sprites = pygame.sprite.Group()
        self.all_sprites = all_sprites
        self.object_sprites = object_sprites

        for object in self.planetSurface.points.values():
            location = object.point
            locationXY = self.latLongToXY((location.latitude, location.longitude))
            objectSprite = SurfaceObjectSprite(object, center=locationXY)
            self.object_sprites.add(objectSprite)
            self.all_sprites.add(objectSprite)

        summary_rect = pygame.Rect(800, 200, 400, 600)
        timing_rect = pygame.Rect(800, 0, 400, 200)

        self.planet_panel = PlanetStatusPanel(summary_rect, manager = manager, model = model)
        self.planet_panel.set_planet(planet)
        self.planet_panel.surface_button.hide()
        self.planet_panel.update()

        self.timing_panel = TimingPanel(timing_rect, manager = manager, timingMaster=model.timingMaster)




    
    def computeRegionColour(self, region):
        if self.selectedObject == region:
            colour = (180, 180, 10)
        else:
            planetClass = self.planetSurface.planetClass
            terrain = self.model.planetSim.planetClassById(planetClass)[region.terrain]
            colour = terrain.colour

        self.regionColours[region.id] = colour

    def renderGlobe(self):
        self.surf.fill((50, 50, 50))

        if self.planetSurface:
            print("Total: ", self.polyCount)
            drawCount = 0
            hideCount = 0
            for id in self.polygons.keys():
                r = self.polygons[id]
                colour = self.regionColours[id]
                for polygon in r:
                    vectors = tuple(vector(v[0], v[1]) for v in polygon)
                    v12 = self.vsum(vectors[0], vectors[1])
                    v123 = self.vsum(v12, vectors[2])

                    meridianV = vector(self.meridian[0], -self.meridian[1])
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
                        rotatedVertex = latLong(r2)
                        #print(rotatedVertex)

                        screenVertex = self.latLongToXY(rotatedVertex)
                        coordinates.append(screenVertex)

                    pygame.draw.polygon(self.surf, colour, coordinates)

            print("Total drawn:", drawCount)
            print("Total hidden:", hideCount)
            print(self.meridian)
        else:
            pygame.draw.circle(self.surf, (250, 250, 50), center = center, radius = self.radius)

    def extractPolygons(self):
        self.polygons = {}
        for r in self.planetSurface.regions.values():
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
    

    def latLongOccluded(self, lat, long):
        v = vector(lat, long)
        meridianV = vector(self.meridian[0], -self.meridian[1])
        if (dot(meridianV, v) <= 0):
            return True
        else:
            return False
        
    def xyToLatLong(self, pos = center):
        (x, y) = (pos[0] - center[0], pos[1] - center[1])
        height = y/self.radius
        if abs(height) > 1.0:
            return (-999, -999)
        
        lat = -math.asin(height)

        width = x/self.radius/math.cos(lat) 
        if abs(width) > 1.0:
            return (999, 999)
        long = math.asin(width) 
        
        return (math.degrees(lat), math.degrees(long) % 360.0)
    
    def latLongToXY(self, pos = (0, 0)):
        (lat, long) = (math.radians(pos[0]), math.radians(pos[1]))
        height = math.sin(-lat)
        y = height * self.radius
        width = math.sin(long)
        x = width * self.radius * math.cos(lat)
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


    def run(self):
        returnCode = 0

        for event in pygame.event.get():
            if event.type == QUIT:
                returnCode = QUIT
                break
            elif event.type == MOUSEBUTTONUP:
                if self.selectedObject:
                    if isinstance(self.selectedObject, SurfaceObjectSprite):
                        self.selectedObject.selected = False
                        self.selectedObject.update()
                    elif isinstance(self.selectedObject, SurfaceRegion):
                        region = self.selectedObject
                        self.selectedObject = None
                        self.computeRegionColour(region)
                        self.renderGlobe()
                    else:
                        print("Should never get here")
                        assert(False)
                    self.selectedObject = None
                    
                pos = pygame.mouse.get_pos()

                clicked_items = [s for s in self.all_sprites if s.rect.collidepoint(pos)] 
                if len(clicked_items):
                    self.selectedObject = clicked_items[0]
                    self.selectedObject.selected = True
                    self.selectedObject.update()
                    continue

                
                (lat, long) = self.xyToLatLong(pos)
                print ((lat, long))
                if (lat, long) == (999, 999):
                    continue
                ###TODO: At least 4 coordinate systems going on here:
                # - X/Y screen coordinates
                # - Rotated latitude/longitude (frame of meridian)
                # - Absolute latitude/longitude (merdian at (0,0), and what all model code uses internally)
                # - x/y/z vector in cartesian coords with origin at center and y axis on (0,0) meridian
                vLatLot = vector(lat, long)
                unrotatedLat = self.yRot(vLatLot, -self.meridian[0])
                unrotatedLong = self.zRot(unrotatedLat, -self.meridian[1])

                (absLat, absLong) = latLong(unrotatedLong)
                print(absLat, absLong)

                ###TODO: This seems to get right region, if it gets one at all, now, but occasionally misses entirely.
                # Think we need a shedload more tests on regionForPoint as there are still some points it misses.
                region = self.planetSurface.regionForPoint(SurfacePoint(absLat, absLong))
                if region:
                    print(region.name)
                    self.selectedObject = region
                    self.computeRegionColour(region)
                    self.renderGlobe()

            elif event.type == MOUSEWHEEL:
                if event.y >= 1:
                    self.radius = max(self.radius-100.0, 100.0)
                elif event.y <= -1:
                    self.radius = min(self.radius+100.0, 800.0)
                self.renderGlobe()
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

            if event.type == UI_BUTTON_PRESSED:
                if self.timing_panel.handle_event(event):
                    pass

            self.manager.process_events(event)

        for object in self.object_sprites:
            (lat, long) = (object.surfaceObject.point.latitude, object.surfaceObject.point.longitude)
            if self.latLongOccluded(lat, long):
                self.all_sprites.remove(object)
            else:
                coordinate = vector(lat, long)
                rotatedLong = self.zRot(coordinate, self.meridian[1])
                rotatedLat = self.yRot(rotatedLong, self.meridian[0])
                rotatedCoordinate = latLong(rotatedLat)                
                screenCoordinate = self.latLongToXY(rotatedCoordinate)
                object.rect.center = screenCoordinate
                self.all_sprites.add(object)

        self.timing_panel.update()

        for entity in self.all_sprites:
            self.surf.blit(entity.surf, entity.rect)

        self.screen.blit(self.surf, pygame.Rect(0, 0, 1200, 800))
        

        return returnCode