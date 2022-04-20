from typing import Optional
from src.utils.program3.variable import Variable
from src.utils.interpreter_utils.scope import Scope


class CallContext:

    def __init__(self):
        self.scopes = [Scope()]

    def get_variable(self, var_name: str) -> Optional[Variable]:

        variable = None
        for i in range(len(self.scopes)):
            variable = self.scopes[i].get_variable(var_name)
            if variable:
                break
        return variable

    def add_scope(self):
        scope = Scope()
        self.scopes.insert(0, scope)

    def delete_scope(self):
        if len(self.scopes) > 0:
            return self.scopes.pop(0)

    def get_scope(self):
        if len(self.scopes) > 0:
            return self.scopes[0]

    def add_variable(self, var: Variable):
        # TODO: Decide into which scope
        self.scopes[0].add_variable(var)
