import techTree

# TODO: Not sure it should be resposibility of this class to be passed tech tree. 
# Think it should just discover instance internally.
class PlayerTech:
    def __init__(self, techTree = None):
        self.discovered = []
        self.techTree = techTree
        self.activeTech = None
        self.progress = 0

    def setActiveTech(self, id):
        tech = self.techTree.nodeById(id)
        self.activeTech = tech
        self.progress = 0

    def _completeTech(self):
        if self.activeTech:
            self.discovered.append(self.activeTech.id)
            self.activeTech = None
        else:
            raise ValueError

    def addResearch(self, increment):
        self.progress += increment
        if self.activeTech and self.progress >= self.activeTech.cost:
            self._completeTech()
            self.progress = 0

