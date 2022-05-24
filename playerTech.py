import techTree

# TODO: Not sure it should be resposibility of this class to be passed tech tree. 
# Think it should just discover instance internally.
class PlayerTech:
    def __init__(self, techTree = None):
        self.discovered = []
        self.techTree = techTree
