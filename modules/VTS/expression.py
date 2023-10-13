# class for expression and array of expressions

class Expression:
    def __init__(self, name, file, active):
        self.name = name
        self.file = file
        self.active = active

    def setState(self, active):
        self.active = active

    
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
        for expression in expressions:
            self.addExpression(expression)
    