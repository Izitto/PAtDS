'''
json save file format:
array of models object with model name, model id and position object
{
    "Model_Positions": [
        {
            "name": "model name",
            "id": "model id",
            "positions": [
                {
                    "name": "position name",
                    "timeInSeconds": "time in seconds",
                    "valuesAreRelativeToModel": "relative",
                    "positionX": "x",
                    "positionY": "y",
                    "rotation": "rotation",
                    "size": "size"
                }
            ]
        }
    ]
}
need classes for Model_Positions, Model_Position, Position
'''

class Position:
    def __init__(self, name, timeInSeconds, valuesAreRelativeToModel, positionX, positionY, rotation, size):
        self.name = name
        self.timeInSeconds = timeInSeconds
        self.valuesAreRelativeToModel = valuesAreRelativeToModel
        self.positionX = positionX
        self.positionY = positionY
        self.rotation = rotation
        self.size = size

    def toJSON(self):
        return {
            "name": self.name,
            "timeInSeconds": self.timeInSeconds,
            "valuesAreRelativeToModel": self.valuesAreRelativeToModel,
            "positionX": self.positionX,
            "positionY": self.positionY,
            "rotation": self.rotation,
            "size": self.size
        }
    
    def toStr(self):
        return str(self.name) + " " + str(self.timeInSeconds) + " " + str(self.valuesAreRelativeToModel) + " " + str(self.positionX) + " " + str(self.positionY) + " " + str(self.rotation) + " " + str(self.size)
    
    def setValues(self, name, timeInSeconds, valuesAreRelativeToModel, positionX, positionY, rotation, size):
        self.name = name
        self.timeInSeconds = timeInSeconds
        self.valuesAreRelativeToModel = valuesAreRelativeToModel
        self.positionX = positionX
        self.positionY = positionY
        self.rotation = rotation
        self.size = size

    def getValues(self):
        return self.name, self.timeInSeconds, self.valuesAreRelativeToModel, self.positionX, self.positionY, self.rotation, self.size
    
class Model_Position:
    def __init__(self, name, id, positions):
        self.name = name
        self.id = id
        self.positions = positions

    def toJSON(self):
        return {
            "name": self.name,
            "id": self.id,
            "positions": [position.toJSON() for position in self.positions]
        }
    
    def toStr(self):
        return str(self.name) + " " + str(self.id) + " " + str(self.positions)
    
    def setValues(self, name, id, positions):
        self.name = name
        self.id = id
        self.positions = positions

    def getValues(self):
        return self.name, self.id, self.positions
    
class Model_Positions:
    def __init__(self):
        self.model_positions: list = []

    def addModel_Position(self, model_position):
        self.model_positions.append(model_position)

    def getModel_Position(self, id):
        for model_position in self.model_positions:
            if model_position.id == id:
                return model_position
            
    def getModel_Positions(self):
        return self.model_positions
    
    def addModel_Positions(self, model_positions_data):
        self.model_positions.clear()
        for mp_data in model_positions_data:
            positions = [Position(**pos) for pos in mp_data['positions']]
            model_position = Model_Position(name=mp_data['name'], id=mp_data['id'], positions=positions)
            self.addModel_Position(model_position)
    
    def toStr(self):
        return str(self.model_positions)
    
    def toJSON(self):
        return [model_position.toJSON() for model_position in self.model_positions]