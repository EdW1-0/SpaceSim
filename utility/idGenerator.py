class IDGenerator:
    def __init__(self):
        self.nextId = 0
        self.ids = set()

    def generateId(self):
        while self.nextId in self.ids:
            self.nextId += 1
        
        return self.setId(self.nextId)
    
    def setId(self, id):
        if id in self.ids:
            raise KeyError
        
        self.ids.add(id)
        return id
    
    def clearId(self, id):
        self.ids.remove(id)
        return id