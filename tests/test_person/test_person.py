import unittest

from personmodel import (
    Person,
    Task,
    TaskCategory
)


class TestPerson(unittest.TestCase):
    def testPerson(self):
        self.assertTrue(Person)
        self.assertTrue(Person(0))

    def testPersonAttributes(self):
        self.assertTrue(hasattr(Person(0), "id"))
        self.assertTrue(hasattr(Person(0), "name"))
        self.assertTrue(hasattr(Person(0), "age"))
        self.assertTrue(hasattr(Person(0), "sex"))
        self.assertTrue(hasattr(Person(0), "task"))

    def testPersonConstructor(self):
        self.assertEqual(Person(5).id, 5)
        self.assertEqual(Person(3, name="John Smith").name, "John Smith")
        self.assertEqual(Person(4, age=66).age, 66)
        self.assertEqual(Person(9, sex="M").sex, "M")


class TestPersonTask(unittest.TestCase):
    def testPersonSetTask(self):
        t = Task(1)
        person = Person(0, name="Dee Jay", age=25, sex="F")
        person.setTask(t)
        self.assertEqual(person.task, t)

    def testPersonTick(self):
        person = Person(0)
        # No return code, just verify doesn't throw an exception
        self.assertEqual(person.tick(1000), None)

    def testPersonTaskProgress(self):
        person = Person(0)
        person.setTask(Task(2))
        person.tick(10)
        self.assertEqual(person.task.progress, 10)

    def testPersonTaskProgressIdle(self):
        person = Person(0)
        person.setTask(Task(TaskCategory.IDLE))
        person.tick(10)
        self.assertEqual(person.task.progress, 0)

    def testPersonTaskCompletion(self):
        person = Person(0)
        person.setTask(Task(TaskCategory.SLEEP))
        person.tick(200)
        self.assertEqual(person.task.category, TaskCategory.IDLE)
