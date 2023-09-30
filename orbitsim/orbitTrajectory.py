from enum import Enum

from planetsim.surfacePoint import SurfacePoint
from planetsim.surfaceBase import SurfaceBase


class TrajectoryState(str, Enum):
    DEFINITION = ("Definition",)
    PENDING = ("Pending",)
    ACTIVE = ("Active",)
    COMPLETE = "Complete"


class OrbitTrajectory:
    def __init__(
        self,
        particleId,
        trajectory,
        state=TrajectoryState.DEFINITION,
        surfaceCoordinates=None,
    ):
        self.particleId = particleId
        self.trajectory = trajectory
        self.state = state
        self.surfaceCoordinates = surfaceCoordinates

    def strRep(self, orbitSim):
        trajectoryText = ""
        trajectoryText += self.state + "<br>"

        for node in self.allNodes():
            orbitNode = orbitSim.nodeById(node)
            trajectoryText += orbitNode.name + "<br>"

        if self.surfaceCoordinates:
            if isinstance(self.surfaceCoordinates, SurfacePoint):
                trajectoryText += str(
                    (
                        self.surfaceCoordinates.latitude,
                        self.surfaceCoordinates.longitude,
                    )
                )
            elif isinstance(self.surfaceCoordinates, SurfaceBase):
                trajectoryText += self.surfaceCoordinates.name

        return trajectoryText

    def nextLink(self, nodeId):
        nodes = [
            self.trajectory[2 * i] for i in range(int(len(self.trajectory) / 2) + 1)
        ]
        index = 2 * nodes.index(nodeId)
        return self.trajectory[index + 1]

    def nextNode(self, linkId):
        links = [
            self.trajectory[2 * i + 1] for i in range(int(len(self.trajectory) / 2))
        ]
        index = 2 * links.index(linkId) + 1
        return self.trajectory[index + 1]

    def allLinks(self):
        return [
            self.trajectory[2 * i + 1] for i in range(int(len(self.trajectory) / 2))
        ]

    def allNodes(self):
        return [
            self.trajectory[2 * i] for i in range(int(len(self.trajectory) / 2) + 1)
        ]
