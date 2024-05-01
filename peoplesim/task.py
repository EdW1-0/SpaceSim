from enum import Enum

from peoplesim.taskClass import TaskClass



class Task:
    def __init__(self, id: str, taskClass: TaskClass = None, target: object=None):
        self.id = id
        self.taskClass = taskClass
        self.progress = 0
        # Target the task is working on
        self.target = target

    def complete(self, actor):
        if self.target:
            self.target.complete()
