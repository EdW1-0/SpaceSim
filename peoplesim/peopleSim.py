from utility import loadEntityFile, IDGenerator
from peoplesim.person import Person

from colonysim import ColonySim, Colony, Ship, Building
from planetsim import PlanetSim, Vehicle
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

        self.personIdGenerator = IDGenerator()

        self._people = loadEntityFile(
            path=jsonPath, 
            id="People", 
            EntityClass=Person, 
            modifiers={"location": [self.locationLoadModifier, "locationClass"]})
        
        for person in self._people.values():
            self.personIdGenerator.setId(person.id)
            if person.location:
                person.location.crew.add(person.id)
        

    def personById(self, id: int) -> Person:
        return self._people[id]
    
    def locationLoadModifier(self, location: int | list[int], locationClass: str):
        if locationClass == "Colony":
            if isinstance(location, int):
                retVal = self.colonySim.colonyById(location) 
            elif isinstance(location, list):
                colony = self.colonySim.colonyById(location[0])
                retVal = colony.buildingById(location[1])
            else:    
                raise ValueError("Invalid location {0}".format(location))
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
    
    def createPerson(self, name: str, age: int=0, sex: str="F", location: Colony | Vehicle | Ship=None) -> int:
        personId = self.personIdGenerator.generateId()
        person = Person(
            id=personId, 
            name=name, 
            age=age,
            sex=sex,
            location=location
            )
        self._people[personId] = person
        location.crew.add(personId)
        return personId
    
    def destroyPerson(self, id: int):
        person = self._people[id]
        person.location.crew.remove(id)
        del self._people[id]
    
    def transferPerson(self, person: Person, location: Colony | Vehicle | Ship | Building):
        person.location.crew.remove(person.id)
        person.location = location
        location.crew.add(person.id)
        
        