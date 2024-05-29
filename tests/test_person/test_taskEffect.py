import unittest

from peoplesim.taskEffect import TaskEffect

class TestTaskEffect(unittest.TestCase):
    def test_taskEffect(self):
        self.assertTrue(TaskEffect)
        taskEffect = TaskEffect()
        self.assertIsInstance(taskEffect, TaskEffect)