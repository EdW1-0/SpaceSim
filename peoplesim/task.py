from enum import Enum


class TaskCategory(Enum):
    IDLE = 0
    SLEEP = 1
    PLANT_WHEAT = 2


class Task:
    def __init__(self, category=TaskCategory.IDLE, target=None):
        self.category = category
        self.progress = 0
        # Target the task is working on, typically a work order
        self.target = target

    def complete(self, actor):
        if self.target:
            self.target.complete()
