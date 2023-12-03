
class GraphNodeClass:
    children = []
    parent = 0
    data: tuple
    def __init__(self):
        # self.parent = parent
        pass
    
    def addChild(self, child):
        self.children.append(child)