from src.utils.program3.variable import Variable


class Scope:

    def __init__(self):
        self.variables = {}

    def add_variable(self, var: Variable):
        self.variables[var.name] = var

    def get_variable(self, name: str) -> Variable:
        return self.variables.get(name)

    def var_exists(self, name: str) -> bool:
        return name in self.variables.keys()