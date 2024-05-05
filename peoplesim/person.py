from peoplesim.task import Task

from colonysim import Colony, Ship
from planetsim import Vehicle

class Person:
    def __init__(self, id: int, name: str="Jane Bloggs", age: int=25, sex: str="F", location: Colony | Ship | Vehicle = None):
        self.id = id
        self.name = name
        self.age = age
        self.sex = sex

        self.location = location

        self.task: Task = None

    def setTask(self, task: Task):
        self.task = task


