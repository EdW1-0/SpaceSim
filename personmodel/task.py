from enum import Enum

class TaskCategory(Enum):
    IDLE = 0
    SLEEP = 1

class Task:
    def __init__(self, category = TaskCategory.IDLE):
        self.category = category
        self.progress = 0