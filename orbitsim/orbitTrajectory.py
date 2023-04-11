class OrbitTrajectory:
    def __init__(self, particleId, trajectory):
        self.particleId = particleId
        self.trajectory = trajectory

    def nextLink(self, nodeId):
        nodes = [self.trajectory[2*i] for i in range(int(len(self.trajectory)/2)+1)]
        index = 2 * nodes.index(nodeId)
        return self.trajectory[index + 1]
    
    def nextNode(self, linkId):
        links = [self.trajectory[2*i + 1] for i in range(int(len(self.trajectory)/2))]
        index = 2 * links.index(linkId) + 1
        return self.trajectory[index + 1]
    
    def allLinks(self):
        return [self.trajectory[2*i + 1] for i in range(int(len(self.trajectory)/2))]
    
    def allNodes(self):
        return [self.trajectory[2*i] for i in range(int(len(self.trajectory)/2)+1)]