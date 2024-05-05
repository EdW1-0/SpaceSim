import unittest
from unittest.mock import MagicMock

from enum import Enum

from peoplesim.task import Task
from peoplesim.taskClass import TaskClass   


class TestTask(unittest.TestCase):
    def setUp(self):
        self.taskClass = TaskClass(0)

    def testTask(self):
        self.assertTrue(Task)
        self.assertTrue(Task(0, self.taskClass))

    def testTaskAttributes(self):
        self.assertTrue(isinstance(Task(0, self.taskClass).taskClass, TaskClass))
        self.assertTrue(isinstance(Task(0, self.taskClass).progress, int))
        self.assertTrue(isinstance(Task(0, self.taskClass).target, object))
        self.assertTrue(hasattr(Task(0, self.taskClass), "assigneeId"))

    def testTaskConstructor(self):
        self.assertTrue(Task(0, self.taskClass))
        self.assertTrue(Task(0, self.taskClass, target=MagicMock()))


# class TestTaskCategory(unittest.TestCase):
#     def testTaskCategoryInit(self):
#         self.assertTrue(TaskCategory)
#         self.assertTrue(TaskCategory(0))

#     def testTaskCategoryIntrospection(self):
#         self.assertTrue(issubclass(TaskCategory, Enum))
#         self.assertTrue(isinstance(TaskCategory.IDLE, TaskCategory))
#         self.assertTrue(isinstance(TaskCategory(1), TaskCategory))

#     def testTaskCategoryEnum(self):
#         self.assertTrue(TaskCategory.IDLE)
#         self.assertTrue(TaskCategory.SLEEP)
#         self.assertTrue(TaskCategory.PLANT_WHEAT)


class WOMock:
    pass


# class TestTaskComplete(unittest.TestCase):
#     def setUp(self):
#         self.womock = WOMock()
#         self.womock.complete = MagicMock()
#         self.task = Task(TaskCategory.PLANT_WHEAT, target=self.womock)

#     def testTaskComplete(self):
#         self.task.complete(None)
#         self.assertTrue(self.womock.complete.called)
