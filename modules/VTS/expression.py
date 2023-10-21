# class for expression and array of expressions

import json
class Expression:
    def __init__(self, name, file, active):
        self.name = name
        self.file = file
        self.active = active

    def setState(self, active):
        self.active = active


    def toStr(self):
        return str(self.file) + " " + str(self.name) + " " + str(self.active)
    
    def toJSON(self):
        return {
            "name": self.name,
            "file": self.file,
            "active": self.active
            }
    

    
class Expressions:
    def __init__(self):
        self.expressions = []

    def addExpression(self, expression):
        self.expressions.append(expression)

    def getExpression(self, file):
        for expression in self.expressions:
            if expression.file == file:
                return expression
            
    def getExpressions(self):
        return self.expressions
    
    def addExpressions(self, expressions):
        self.expressions.clear()
        for expression in expressions:
            self.addExpression(expression)

    def setExpressionStatus(self, file, active):
        for expression in self.expressions:
            if expression.file == file:
                expression.setState(active)

    def toStr(self):
        return str(self.expressions)
    
    def toJSON(self):
        return [expression.toJSON() for expression in self.expressions]