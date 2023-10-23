# object for saved position for model
'''
example:
"data": {
		"timeInSeconds": 0.2,
		"valuesAreRelativeToModel": false,
		"positionX": 0.1,
		"positionY": -0.7,
		"rotation": 16.3,
		"size": -22.5
	}
'''

class Position:
    def __init__(self):
        self.modelID
        self.name
        self.timeInSeconds
        self.valuesAreRelativeToModel
        self.positionX
        self.positionY
        self.rotation
        self.size

    def toStr(self):
        return str(self.positionX) + " " + str(self.positionY) + " " + str(self.rotation) + " " + str(self.size)
    
    def toJSON(self):
        return {
            "modelID": self.modelID,
            "name": self.name,
            "timeInSeconds": self.timeInSeconds,
            "valuesAreRelativeToModel": self.valuesAreRelativeToModel,
            "positionX": self.positionX,
            "positionY": self.positionY,
            "rotation": self.rotation,
            "size": self.size
            }

    def getCoords(self):
        return self.positionX, self.positionY, self.rotation, self.size


