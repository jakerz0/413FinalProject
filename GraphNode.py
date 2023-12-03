
class GraphNode:
    children = []
    parent = 0
    def __init__(self, parent):
        self.parent = parent
        pass

    def addChild(self, child):
        self.children.append(child)