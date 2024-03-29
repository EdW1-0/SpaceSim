from techtree import TechTree, PlayerTech
from orbitsim import OrbitSim
from colonysim import ColonySim
from planetsim import PlanetSim
from peoplesim import PeopleSim
from timingMaster import TimingMaster
from playerState import PlayerState

import pickle

class GameModel:
    # Needs:
    # Set of orbits
    # Planet surfaces
    # Tech tree
    # People
    def __init__(self):
        self.techTree: TechTree = None
        self.playerTech: PlayerTech = None
        self.orbitSim: OrbitSim = None
        self.planetSim: PlanetSim = None
        self.timingMaster: TimingMaster = None
        self.colonySim: ColonySim = None
        self.planetSim: PlanetSim = None
        self.init = False

    def load(self, jsonRoot="json", reload=False):
        if not reload and self.init:
            print("Already loaded")
            return

        # TODO: Wrap these in a try/catch to do special exception handling
        # rather than just the default file errors.
        self.playerState = PlayerState()

        self.techTree = TechTree(jsonRoot + "/Technologies.json")
        self.playerTech = PlayerTech(self.techTree)
        self.playerTech.parameterModifierCallback = self.playerState.applyModifier

        self.orbitSim = OrbitSim(
            jsonRoot + "/Orbits.json", jsonRoot + "/Particles.json", playerState=self.playerState
        )
        self.planetSim = PlanetSim(
            self.orbitSim,
            self.playerState,
            jsonRoot + "/Planets.json",
            vehicleClassPath="json/vehicleClasses",
        )

        self.colonySim = ColonySim(
            self.orbitSim,
            self.planetSim,
            self.playerTech,
            self.playerState,
            jsonRoot + "/planets/colonies",
            vehicleFactory=self.planetSim.createVehicle
        )

        self.orbitSim.landCallback = self.planetSim.landShip

        self.orbitSim.validatePlanets(self.planetSim)

        self.peopleSim = PeopleSim(
            colonySim=self.colonySim,
            planetSim=self.planetSim,
            orbitSim=self.orbitSim,
        )

        self.timingMaster = TimingMaster(0)
        # If we got here all the module loads succeeded so set our init flag
        self.init = True

    def saveModel(self, file):
        saveArray = [self.techTree, self.orbitSim, self.planetSim, self.colonySim, self.timingMaster]

        pickle.dump(saveArray, file)

    def loadModel(self, file):
        loadArray = pickle.load(file)
        self.techTree = loadArray[0]
        self.orbitSim = loadArray[1]
        self.planetSim = loadArray[2]
        self.colonySim = loadArray[3]
        self.timingMaster = loadArray[4]
        self.init = True

    def get_init(self):
        return self.init

    def validateModel(self):
        if not (self.techTree and self.colonySim and self.orbitSim and self.planetSim and self.timingMaster):
            return False
        
        if len(self.orbitSim._nodes) > 0:
            return True
        else:
            return False
        


    def tick(self):
        if not self.timingMaster:
            return

        start = self.timingMaster.timestamp
        self.timingMaster.tick()
        end = self.timingMaster.timestamp

        increment = end - start
        if increment:
            self.techTree.tick(increment)
            self.playerTech.tick(increment)
            self.orbitSim.tick(increment)
            self.planetSim.tick(increment)
            self.colonySim.tick(increment)
