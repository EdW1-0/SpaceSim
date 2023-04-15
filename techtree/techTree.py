import os
import json
from dataclasses import dataclass
from enum import Enum

import techtree.techNode as techNode

class TechEffectClass(Enum):
    BUILDING = 0
    VEHICLE = 1

@dataclass
class TechEffect:
    effect: TechEffectClass
    value: int


# TODO: Make a singleton. I think we just make a class variable to store it and add to it
# if needed. Maybe reinitialise if jsonPath changes.
class TechTree:
    def __init__(self, jsonPath = "json/Technologies.json"):
        jsonFile = open(jsonPath, "r")
        jsonTechs = json.load(jsonFile)

        jsonNodes = jsonTechs["Technologies"]

        self.nodes = {node["id"]: techNode.TechNode(**node) for node in jsonNodes}
        self.totalNodes = len(self.nodes)

        # Validate no duplicate ids 
        assert(self.totalNodes == len(jsonNodes))

        # Validate ancestors - check every ancestor points to a real key
        for node in self.nodes:
            for ancestor in self.nodeById(node).ancestors:
                assert(ancestor in self.nodes)

        # Not optimal - we recheck many nodes by setting up checked afresh on every node. Probably a faster way to do this, but 
        # we only need to do this check once, at load time, so may be tolerable.
        def cycleCheck(node, checked):
            assert(node.id not in checked)
            checked.add(node.id)

            for ancestor in node.ancestors:
                # Note we don't care if we reach an ancestor by 2 independent routes,
                # so don't keep checked state from ancestor branches, only descendents
                branchChecked = checked.copy()
                cycleCheck(self.nodeById(ancestor), branchChecked)
        
        for node in self.nodes.values():
            checked = set()
            cycleCheck(node, checked)

        jsonFile.close()



    def nodeById(self, id):
        if not isinstance(id, int):
            raise TypeError
        elif id < 0:
            raise ValueError
        return self.nodes[id]

    def ancestorsOfId(self, id):
        node = self.nodeById(id)
        return [self.nodeById(ancestor) for ancestor in node.ancestors]

    def descendentsOfId(self, id):
        return [node for node in self.nodes.values() if id in node.ancestors]
    
    def tick(self, increment):
        # Intentionally does nothing - this is supposed to be a static object store. 
        pass
