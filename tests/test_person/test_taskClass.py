import unittest

from peoplesim.taskClass import TaskClass

class TestTaskClass(unittest.TestCase):
    def testTaskClass(self):
        self.assertTrue(TaskClass)
        self.assertTrue(TaskClass(0))

    def testTaskClassConstructor(self):
        self.assertTrue(TaskClass(id = "SLEEP", name = "Sleep", inputs = [], duration = 8, effects = []))
        with self.assertRaises(TypeError):
            TaskClass()

    def testTaskClassAttributes(self):
        self.assertTrue(hasattr(TaskClass("SLEEP"), "id"))
        self.assertTrue(hasattr(TaskClass(0), "name"))
        self.assertTrue(hasattr(TaskClass(0), "inputs"))
        self.assertTrue(hasattr(TaskClass(0), "duration"))
        self.assertTrue(hasattr(TaskClass(0), "effects"))

