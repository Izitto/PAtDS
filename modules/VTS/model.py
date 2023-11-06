import json
# class for models and array of models


class Model:
    def __init__(self, name, id, active):
        self.name = name
        self.id = id
        self.active = active

    def setState(self, active):
        self.active = active

    def toStr(self):
        return str(self.id) + " " + str(self.name) + " " + str(self.active)

    def toJSON(self):
        return {
            "name": self.name,
            "id": self.id,
            "active": self.active
        }


class Models:
    def __init__(self):
        self.models: list = []

    def addModel(self, model):
        self.models.append(model)

    def getModel(self, id):
        for model in self.models:
            if model.id == id:
                return model

    def getModels(self):
        return self.models

    def addModels(self, models):
        self.models.clear()
        for model in models:
            self.addModel(model)

    def setModelSatus(self, id, active):
        for model in self.models:
            if model.id == id:
                model.setState(active)
                return True
        return False

    # get active model id

    def getActiveModel(self):
        for model in self.models:
            if model.active == True:
                return model.id
        return None

    def toStr(self):
        return str(self.models)
    
    def toJSON(self):
        return [model.toJSON() for model in self.models]
    
    def getActiveModelIDandName(self):
        for model in self.models:
            if model.active == True:
                return model.id, model.name
        return None, None