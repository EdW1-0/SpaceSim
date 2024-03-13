from utility import loadEntityFile
from peoplesim.person import Person

from colonysim import ColonySim
from planetsim import PlanetSim
from orbitsim import OrbitSim

class PeopleSim:
    def __init__(
            self, 
            jsonPath: str = "json/people", 
            colonySim: ColonySim = None, 
            planetSim: PlanetSim = None, 
            orbitSim: OrbitSim = None
            ):
        
        self.colonySim = colonySim
        self.planetSim = planetSim
        self.orbitSim = orbitSim

        self._people = loadEntityFile(
            path=jsonPath, 
            id="People", 
            EntityClass=Person, 
            modifiers={"location": [self.locationLoadModifier, "locationClass"]})
        
        for person in self._people.values():
            if person.location:
                person.location.crew.add(person.id)
        
        # for person in self._people.values():
        #     if person.location == "Colony":
        #         person
        #     person.location.crew.add(person.id)s


    def personById(self, id: int) -> Person:
        return self._people[id]
    
    def locationLoadModifier(self, location: int, locationClass: str):
        if locationClass == "Colony":
            retVal = self.colonySim.colonyById(location) 
        elif locationClass == "Ship":
            if self.orbitSim:
                retVal = self.orbitSim.shipById(location)
            else:
                raise NotImplementedError
        elif locationClass == "Vehicle":
            if self.planetSim:
                retVal = self.planetSim.vehicleById(location)
            else:
                raise NotImplementedError
        else:
            raise ValueError("Invalid location class {0}".format(locationClass))
        
        return retVal
        