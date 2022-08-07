import unittest

from enum import Enum

from personmodel.task import Task, TaskCategory

class TestTask(unittest.TestCase):
    def testTask(self):
        self.assertTrue(Task)
        self.assertTrue(Task())

    def testTaskAttributes(self):
        attrs = ["category", "progress"]
        for a in attrs:
            self.assertTrue(hasattr(Task(), a))

        self.assertTrue(isinstance(Task().category, TaskCategory))
        self.assertTrue(isinstance(Task().progress, int))

    def testTaskConstructor(self):
        self.assertEqual(Task(TaskCategory.SLEEP).category, TaskCategory.SLEEP)

class TestTaskCategory(unittest.TestCase):
    def testTaskCategoryInit(self):
        self.assertTrue(TaskCategory)
        self.assertTrue(TaskCategory(0))

    def testTaskCategoryIntrospection(self):
        self.assertTrue(issubclass(TaskCategory, Enum))
        self.assertTrue(isinstance(TaskCategory.IDLE, TaskCategory))
        self.assertTrue(isinstance(TaskCategory(1), TaskCategory))