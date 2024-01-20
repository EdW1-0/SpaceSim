import json
import os
from inspect import isclass


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
                        if isinstance(altClasses[altId], tuple):
                            ac = altClasses[altId][0]
                            aargs = altClasses[altId][1]
                            entityDict.update({e["id"]: ac(**e, **kwargs, **aargs)})
                        elif isclass(altClasses[altId]):
                            entityDict.update({e["id"]: altClasses[altId](**e, **kwargs)})
                        else:
                            print("Unknown altClasses argument: ", altClasses[altId])
                            raise TypeError
                        foundAlt = True
                        break
                if not foundAlt:
                    entityDict.update({e["id"]: EntityClass(**e, **kwargs)})
    return entityDict
