from personmodel.task import Task, TaskCategory

class Person:
    def __init__(self, id, name = "Jane Bloggs", age = 25, sex = "F"):
        self.id = id
        self.name = name
        self.age = age
        self.sex = sex

        self.task = Task(TaskCategory.IDLE)

    def setTask(self, task):
        self.task = task

    def tick(self, increment):
        # Some tasks are placeholders and will never be complete. Later should make this more sophisticated to
        # Handle other cases.
        if self.task.category == TaskCategory.IDLE:
            return
        while increment:
            if self.task.progress + increment < 100:
                self.task.progress += increment
                increment = 0
            else:
                increment -= (100 - self.task.progress)
                self.completeTask()

    def completeTask(self):
        # Trigger task complete
        # Apply any back effects
        # Delete task
        self.task.complete(self)
        self.task = Task(TaskCategory.IDLE)