from utility import loadEntityFile, IDGenerator
from peoplesim.person import Person
from peoplesim.taskClass import TaskClass
from peoplesim.task import Task
from peoplesim.taskEffect import TaskEffectStateChange, TaskEffectParameter

from colonysim import ColonySim, Colony, Ship, Building, BuildingStatus
from planetsim import PlanetSim, Vehicle
from orbitsim import OrbitSim

class PeopleSim:
    def __init__(
            self, 
            jsonPath: str = "json/people", 
            taskClassPath: str = "json/tasks",
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

        self._taskClasses = loadEntityFile(
            path=taskClassPath,
            id="Tasks",
            EntityClass=TaskClass
        )

        self.taskQueue = {}
        self.taskIdGenerator = IDGenerator()
        

    def personById(self, id: int) -> Person:
        return self._people[id]
    
    def taskById(self, id: int) -> Task:
        return self.taskQueue[id]
    
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
        
    def createTask(self, taskClassId: str, target: Colony | Vehicle | Ship | Building | Person):
        taskClass = self._taskClasses[taskClassId]
        taskId = self.taskIdGenerator.generateId()
        task = Task(id=taskId, taskClass=taskClass, target=target)
        self.taskQueue[taskId] = task
        return taskId
    
    def assignTask(self, task: Task, person: Person):
        if task.assigneeId:
            oldAssignee = self._people[task.assigneeId]
            oldAssignee.task = None

        if person.task:
            oldTask = person.task
            oldTask.assigneeId = None

        task.assigneeId = person.id
        person.task = task


    def completeTask(self, task: Task):
        # Trigger task complete
        # Apply any back effects
        # Delete task
        #self.task.complete(self)
        for effect in task.taskClass.effects:
            if isinstance(effect, TaskEffectStateChange):
                setattr(task.target, effect.state, effect.value)
            if isinstance(effect, TaskEffectParameter):
                setattr(task.target, effect.parameter, effect.amount)


        person = self._people[task.assigneeId]
        person.task = None
        del self.taskQueue[task.id]
        

    def generateTasks(self):
        for colony in self.colonySim._colonies.values():
            for building in colony.buildings.values():
                if building.status == BuildingStatus.CONSTRUCTION:
                    task = None
                    for t in self.taskQueue.values():
                        if t.target == building:
                            task = t
                            break
                    if not task:
                        self.createTask("BUILD", building)

    def tick(self):
        # What this needs to do:
         #  - Check for new tasks to make
        # - Tick each person so they update passive interactions
        # - Check the task queue and assign any tasks that are not assigned
        # - Tick each task so they update progress

        # Decisions here:
        # - How do we track which tasks have been assigned to whom?
        # - Where do we store tasks? Do we pull them off queue when assigned?
        # For now - I think store task reference in person object and store person id in task object
        # Mediate task assignment through dedicated method responsible for cleaning this up.
        # For now, stick everything on task queue. Later, we can optimize this, and implement a priority queue.
        # 1 - Handle task assignment
        self.generateTasks()

        for task in self.taskQueue.values():
            if task.assigneeId is not None:
                continue

            for person in self._people.values():
                if not person.task:
                    self.assignTask(task, person)
                    break
        
        # 2 - Update progress on tasks
        for person in self._people.values():
            if person.task:
                person.task.progress += 1
                if person.task.progress >= person.task.taskClass.duration:
                    self.completeTask(person.task)

