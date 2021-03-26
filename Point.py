class Point():
    def __init__(self, x, y, elev, terrain):
        self.x = x
        self.y = y
        self.elev = elev
        self.terrain = terrain
        self.parent = None
        self.gn = 0.0
        self.hn = 0.0
        
    def setgn(self, gn):
        self.gn = gn
        
    def sethn(self, hn):
        self.hn = hn
        
    def setTerrain(self, ter):
        self.terrain = ter
        
    def setParent(self, parent):
        self.parent = parent