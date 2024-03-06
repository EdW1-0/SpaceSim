from peoplesim.task import Task, TaskCategory

from colonysim import Colony, Ship
from planetsim import Vehicle

class Person:
    def __init__(self, id: int, name: str="Jane Bloggs", age: int=25, sex: str="F", location: Colony | Ship | Vehicle = None):
        self.id = id
        self.name = name
        self.age = age
        self.sex = sex

        self.location = location

        self.task: Task = Task(TaskCategory.IDLE)

    def setTask(self, task: Task):
        self.task = task

    def tick(self, increment: int):
        # Some tasks are placeholders and will never be complete.
        # Later should make this more sophisticated to
        # Handle other cases.
        if self.task.category == TaskCategory.IDLE:
            return
        while increment:
            if self.task.progress + increment < 100:
                self.task.progress += increment
                increment = 0
            else:
                increment -= 100 - self.task.progress
                self.completeTask()

    def completeTask(self):
        # Trigger task complete
        # Apply any back effects
        # Delete task
        self.task.complete(self)
        self.task = Task(TaskCategory.IDLE)
