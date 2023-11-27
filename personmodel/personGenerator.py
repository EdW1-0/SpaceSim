import random
import json

from personmodel.person import Person

from utility import IDGenerator


class PersonGenerator:
    def __init__(self, path="test_json/test_person"):
        (surnameFile, maleFile, femaleFile) = (
            open(path + fn, "r")
            for fn in ("/surnames.json", "/male_names.json", "/female_names.json")
        )
        (surnameJson, maleJson, femaleJson) = (
            json.load(f) for f in (surnameFile, maleFile, femaleFile)
        )
        (self.surnames, self.male_names, self.female_names) = (
            j["Names"] for j in (surnameJson, maleJson, femaleJson)
        )
        [f.close() for f in (surnameFile, maleFile, femaleFile)]

        self.personIdGenerator = IDGenerator()

    def newPerson(self):
        sexes = ("M", "F")
        sex = random.choice(sexes)
        age = random.randrange(20, 50)
        if sex == "M":
            forename = random.choice(self.male_names)
        else:
            forename = random.choice(self.female_names)
        surname = random.choice(self.surnames)
        name = forename + " " + surname
        return Person(self.personIdGenerator.generateId(), name=name, sex=sex, age=age)
