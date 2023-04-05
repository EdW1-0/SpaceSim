import json

from orbitsim.orbitNode import OrbitNode
from orbitsim.orbitLink import OrbitLink
from orbitsim.particle import Particle, DeltaVError
from orbitsim.orbitTrajectory import OrbitTrajectory

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

        # Unpack the nodes into self._nodes; use this rather than comprehension because we need to check for duplicates
        self._nodes = {}
        for node in orbitalsDelinked:
            if node["id"] in self._nodes:
                firstNode = self._nodes[node["id"]].name
                secondNode = node["name"]
                raise KeyError("Orbits file contains duplicate nodes {0} and {1} with same id {2})".format(firstNode, secondNode, node["id"]))
            else:
                self._nodes[node["id"]] = OrbitNode(**node)
            

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

        self._trajectories = {}

    def validatePlanets(self, planetSim):
        for node in self._nodes.values():
            if node.planet:
                assert(node.planet in planetSim.planets.keys())


    def newParticleId(self):
        nodeIdCounter = 0
        while True:
            yield nodeIdCounter
            nodeIdCounter += 1

    def createParticle(self, node, payload = None):
        id = next(self.idGenerator)
        self._particles[id] = Particle(id, payload = payload)
        if(isinstance(node, OrbitNode)):
            node.particles.add(id)
            return id
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

    def createTrajectory(self, targetId, particleId = None, sourceId = None, payload = None):
        if particleId is not None:
            try:
                self.trajectoryForParticle(particleId)
            except KeyError:
                sourceId = self._particleLocation(particleId).id
            else:
                raise KeyError("Particle has existing trajectory")

        elif sourceId is None:
            raise ValueError("Insufficient parameters to construct trajectory")

        paths = self._findPath(sourceId, targetId, [])

        # This seems to do the right thing if paths is empty, not sure this is pythonic though
        if not paths:
            raise ValueError("No valid path found between endpoints")

        if particleId is None:
            particleId = self.createParticle(self.nodeById(sourceId), payload)

        minDv = None
        minPath = []
        for path in paths:
            dv = self._deltaVCost(path)
            if (minDv is None) or (dv < minDv):
                minDv = dv
                minPath = path

        ot = OrbitTrajectory(particleId, minPath)
        #Key the trajectory using the particleId. This ensures 1-1 mapping. 
        self._trajectories[particleId] = ot
        return ot

    def cancelTrajectory(self, id):
        location = self._particleLocation(id)
        # If on a node, can cancel immediately. Otherwise should target next node and stop there.
        if (isinstance(location, OrbitNode)):
            t = self.trajectoryForParticle(id)
            t.trajectory = [location.id]
        else:
            t = self.trajectoryForParticle(id)
            p = self.particleById(id)
            if (p.velocity > 0):
                t.trajectory = [location.bottomNode, location.id, location.topNode]
            else:
                t.trajectory = [location.topNode, location.id, location.bottomNode]

        self._pruneTrajectories()

    def _pruneTrajectories(self):
        def isTerminal(t):
            location = self._particleLocation(t.particleId)
            if (isinstance(location, OrbitNode)) and (location.id is t.trajectory[-1]):
                return True
            else:
                return False

        self._trajectories = {t: self._trajectories[t] for t in self._trajectories if (not isTerminal(self.trajectoryForParticle(t)))}



    def tick(self, increment):
        for t in self._trajectories.values():
            timeBudget = increment
            while timeBudget > 0:
                location = self._particleLocation(t.particleId)
                if isinstance(location, OrbitNode):
                    if (location.id is t.trajectory[-1]):
                        timeBudget = 0
                        continue

                    linkId = t.nextLink(location.id)

                    deltaVCost = self.linkById(linkId).deltaV
                    particle = self.particleById(t.particleId)
                    try:
                        particle.burnDeltaV(deltaVCost)
                    except DeltaVError:
                        timeBudget = 0
                        continue
                    else:
                        self.transitParticle(t.particleId, linkId)

                elif isinstance(location, OrbitLink):
                    particle = self.particleById(t.particleId)
                    delta = timeBudget * particle.velocity
                    newTime = location.particles[t.particleId] + delta
                    if newTime < 0:
                        timeBudget = (newTime/particle.velocity)
                        self.transitParticle(t.particleId, location.bottomNode)
                    elif newTime > location.travelTime:
                        timeBudget = int((newTime - location.travelTime)/particle.velocity)
                        self.transitParticle(t.particleId, location.topNode)
                    else:
                        location.particles[t.particleId] += delta
                        timeBudget = 0

        self._pruneTrajectories()


    def _findPath(self, sourceId, targetId, priorPath):
        path = [*priorPath, sourceId]
        if sourceId == targetId:
            return [path]

        sourceNode = self.nodeById(sourceId)
        validPaths = []
        for linkId in sourceNode.links:
            # Don't traverse links we have already traversed in this path
            checkedLinks = [path[2*i+1] for i in range(int(len(path)/2))]
            if linkId not in checkedLinks:
                nextPath = [*path, linkId]
                link = self.linkById(linkId)
                if sourceId == link.bottomNode:
                    nextId = link.topNode
                elif sourceId == link.topNode:
                    nextId = link.bottomNode
                else:
                    assert False, "Invalid link id for this node!"
                # Reject paths with redundant loops
                checkedNodes = [path[2*i] for i in range(int(len(path)/2))]
                # Note we use in rather than direct equivalence - not perfect but here I think it's OK because we literally are 
                # looking for the same id (so the same object, not just the same value). And the code to check properly would be
                # ugly without actually covering any additional functionality.
                if nextId not in checkedNodes:
                    paths = self._findPath(nextId, targetId, nextPath)
                    for p in paths:
                        validPaths.append(p)

        return validPaths

        # Given prior path
        # Get node
        # Append node id to path
        # If node is target, return path
        # Get all links for node
        # For each unchecked link, append link id, call self on endpoint
        # Collate array of subarrays
        # Return arrays

    def _deltaVCost(self, path):
        dv = 0
        for i in range(int(len(path)/2)):
            dv += self.linkById(path[2*i+1]).deltaV
        return dv



        
    def _particleLocation(self, id):
        for n in self._nodes.values():
            if id in n.particles:
                return n

        for l in self._links.values():
            if id in l.particles.keys():
                return l

        raise KeyError
        

    def nodeById(self, id):
        if not (type(id) == int or isinstance(id, str)):
            raise TypeError
        elif isinstance(id, str) and not id.isupper():
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
    
    def trajectoryForParticle(self, particleId):
        if not isinstance(particleId, int):
            raise TypeError
        elif particleId < 0:
            raise ValueError
        return self._trajectories[particleId]


