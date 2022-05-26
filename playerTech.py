import techTree

# TODO: Not sure it should be resposibility of this class to be passed tech tree. 
# Think it should just discover instance internally.
class PlayerTech:
    def __init__(self, techTree = None):
        self._discovered = set()
        self.techTree = techTree
        self.activeTech = None
        self.progress = 0

    def setActiveTech(self, id):
        tech = self.techTree.nodeById(id)
        self.activeTech = tech
        self.progress = 0

    def _completeTech(self):
        if self.activeTech:
            self._discovered.add(self.activeTech.id)
            self.activeTech = None
        else:
            raise ValueError

    def addResearch(self, increment):
        self.progress += increment
        if self.activeTech and self.progress >= self.activeTech.cost:
            self._completeTech()
            self.progress = 0

    @property
    def discovered(self):
        return self._discovered

    @property
    def possibleTargets(self):
        targets = set()
        #For each tech in tree
        for id in self.techTree.nodes.keys():
            # If discovered, reject
            if id not in self._discovered:
                # Else for each tech in ancestors
                ancestorsDiscovered = True
                for ancestor in self.techTree.nodeById(id).ancestors:
                    # If not in discovered, reject
                    if ancestor not in self._discovered:
                        ancestorsDiscovered = False

                if ancestorsDiscovered:
                    targets.add(id)
            
        return targets




