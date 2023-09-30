import unittest

from personmodel.personGenerator import PersonGenerator
from personmodel.person import Person


class TestPersonGenerator(unittest.TestCase):
    def testPersonGenerator(self):
        self.assertTrue(PersonGenerator)
        self.assertTrue(PersonGenerator())

    def testPersonGeneratorOutput(self):
        self.assertTrue(isinstance(PersonGenerator().newPerson(), Person))

    def testPersonGeneratorLoading(self):
        with self.assertRaises(FileNotFoundError):
            self.assertTrue(PersonGenerator("test_json"))
        self.assertTrue(PersonGenerator("test_json/test_person"))


class TestPersonGeneratorStatistics(unittest.TestCase):
    def setUp(self):
        self.people = {}
        self.pg = PersonGenerator()
        for i in range(50):
            p = self.pg.newPerson()
            self.people[p.id] = p

    def testPersonGeneratorUniqueIds(self):
        self.assertEqual(len(self.people.keys()), 50)

    def testPersonGeneratorSex(self):
        male = 0
        female = 0
        for p in self.people.values():
            if p.sex is "M":
                male += 1
            elif p.sex is "F":
                female += 1

        # OK, so there is a statistical chance of a false positive here. Chance of 50 consecutive M or F is 2* 1/2**N for N gives ~10-16. I'll take it.
        self.assertTrue(male)
        self.assertTrue(female)
        self.assertEqual(male + female, 50)

    def testPersonGeneratorAge(self):
        uniques = set()
        for p in self.people.values():
            uniques.add(p.age)

        self.assertGreater(len(uniques), 1)

    def testPersonGeneratorName(self):
        uniquemale = set()
        uniquefemale = set()
        for p in self.people.values():
            self.assertEqual(len(p.name.split()), 2)
            if p.sex == "M":
                uniquemale.add(p.name)
            else:
                uniquefemale.add(p.name)

        self.assertGreater(len(uniquemale), 1)
        self.assertGreater(len(uniquefemale), 1)

        self.assertEqual(len(uniquemale.intersection(uniquefemale)), 0)
