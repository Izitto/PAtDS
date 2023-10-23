# Desc: Class for storing coordinates


class Coords:
    def __init__(self):
        self.positionX = 0
        self.positionY = 0
        self.rotation = 0
        self.size = 0

    def toStr(self):
        return str(self.positionX) + " " + str(self.positionY) + " " + str(self.rotation) + " " + str(self.size)
    
    def toJSON(self):
        return {
            "positionX": self.positionX,
            "positionY": self.positionY,
            "rotation": self.rotation,
            "size": self.size
            }
    
    def setCoords(self, x, y, rot, size):
        self.positionX = x
        self.positionY = y
        self.rotation = rot
        self.size = size

    def getCoords(self):
        return self.positionX, self.positionY, self.rotation, self.size