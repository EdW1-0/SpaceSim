
def getIntId(id, sourceDict):
    if not isinstance(id, int):
        raise TypeError
    elif id < 0:
        raise ValueError
    return sourceDict[id]

def getStringId(id, sourceDict):
    if not (type(id) == int or isinstance(id, str)):
        raise TypeError
    elif isinstance(id, str) and not id.isupper():
        raise ValueError
    return sourceDict[id]