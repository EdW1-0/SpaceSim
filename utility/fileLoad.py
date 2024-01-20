import json
import os


def extractEntityJson(path, id):
    entityFile = open(path, "r")
    entityJson = json.load(entityFile)
    if id in entityJson:
        entities = entityJson[id]
    else:
        entities = []
    entityFile.close()
    return entities


def loadEntityFile(path: str, id, EntityClass, altClasses={}, **kwargs):
    entityDict = {}
    for subdir, dirs, files in os.walk(path):
        for file in files:
            entities = extractEntityJson(path + "/" + file, id)
            for e in entities:
                foundAlt = False
                for altId in altClasses:
                    if altId in e:
                        entityDict.update({e["id"]: altClasses[altId](**e, **kwargs)})
                        foundAlt = True
                        break
                if not foundAlt:
                    entityDict.update({e["id"]: EntityClass(**e, **kwargs)})
    return entityDict
