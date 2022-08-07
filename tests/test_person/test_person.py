import unittest

from personmodel.person import Person
from personmodel.task import Task

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
        self.assertEqual(Person(3, name = "John Smith").name, "John Smith")
        self.assertEqual(Person(4, age = 66).age, 66)
        self.assertEqual(Person(9, sex = "M").sex, "M")

class TestPersonTask(unittest.TestCase):
    def testPersonSetTask(self):
        t = Task(1)
        person = Person(0, name = "Dee Jay", age = 25, sex = "F")
        person.setTask(t)
        self.assertEqual(person.task, t)
