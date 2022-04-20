from typing import Optional
from src.utils.program3.variable import Variable


class Scope:

    def __init__(self):
        self.variables = {}

    def get_variable(self, variable_name: str) -> Optional[Variable]:
        return self.variables.get(variable_name)

    def add_variable(self, var: Variable):
        self.variables[var.name] = var
