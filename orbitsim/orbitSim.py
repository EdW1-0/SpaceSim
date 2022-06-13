import json

from orbitsim.orbitNode import OrbitNode
from orbitsim.orbitLink import OrbitLink
from orbitsim.particle import Particle

class OrbitSim:
    def __init__(self, jsonPath = "json/Orbits.json"):
        jsonFile = open(jsonPath, "r")

        jsonBlob = json.load(jsonFile)

        orbitalsArray = jsonBlob["Orbitals"]

        def stripLinks(x):
            if "links" in x:
                del x["links"]
            return x
        orbitalsDelinked = [stripLinks(orbital.copy()) for orbital in  orbitalsArray]
        self._nodes = {node["id"]: OrbitNode(**node) for node in orbitalsDelinked}

        self._links = {}
        linkIdCount = 0
        for orbital in orbitalsArray:
            if "links" in orbital:
                for link in orbital["links"]:
                    sourceId = orbital["id"]
                    destId = link["id"] 
                    del link["id"]
                    self._links[linkIdCount] = OrbitLink(id = linkIdCount, bottomNode = sourceId, topNode = destId, **link)
                    self.nodeById(sourceId).links.append(linkIdCount)
                    self.nodeById(destId).links.append(linkIdCount)
                    linkIdCount += 1


        # for each orbital
        # if it has links
        # for each link
        # create a link object
        # add it to our array
        # add link id to links for source and destination

        self._particles = {}
        self.idGenerator = self.newParticleId()

    def newParticleId(self):
        nodeIdCounter = 0
        while True:
            yield nodeIdCounter
            nodeIdCounter += 1

    def createParticle(self, node):
        id = next(self.idGenerator)
        self._particles[id] = Particle(id)
        if(isinstance(node, OrbitNode)):
            node.particles.add(id)
        else:
            raise TypeError

    def destroyParticle(self, id):
        location = self._particleLocation(id)
        location.particles.remove(id)
        del self._particles[id]

    def transitParticle(self, id, targetId):
        location = self._particleLocation(id)
        particle = self.particleById(id)
        if isinstance(location, OrbitNode):
            target = self.linkById(targetId)
            if location.id == target.bottomNode:
                target.particles[id] = 0
                particle.velocity = 1
            elif location.id == target.topNode:
                target.particles[id] = target.travelTime
                particle.velocity = -1
            else:
                raise ValueError

            location.particles.remove(id)

        else:
            target = self.nodeById(targetId)
            if (location.id in target.links):
                target.particles.add(id)
                particle.velocity = 0
                del location.particles[id]
            else:
                raise ValueError

    def tick(self, increment):
        for p in self._particles.values():
            location = self._particleLocation(p.id)
            if isinstance(location, OrbitLink):
                location.particles[p.id] += p.velocity * increment

                if location.particles[p.id] > location.travelTime:
                    self.transitParticle(p.id, location.topNode)
                elif location.particles[p.id] < 0:
                    self.transitParticle(p.id, location.bottomNode)


        
    def _particleLocation(self, id):
        for n in self._nodes.values():
            if id in n.particles:
                return n

        for l in self._links.values():
            if id in l.particles.keys():
                return l

        raise KeyError
        

    def nodeById(self, id):
        if not isinstance(id, int):
            raise TypeError
        elif id < 0:
            raise ValueError
        return self._nodes[id]

    def linkById(self, id):
        if not isinstance(id, int):
            raise TypeError
        elif id < 0:
            raise ValueError
        return self._links[id]

    def particleById(self, id):
        if not isinstance(id, int):
            raise TypeError
        elif id < 0:
            raise ValueError
        return self._particles[id]