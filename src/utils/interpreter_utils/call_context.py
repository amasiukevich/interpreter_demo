from collections import deque
from .scope import Scope
from src.utils.program3.variable import Variable


class CallContext:

    def __init__(self, scope=None):
        self.scopes = deque()
        if not scope:
            scope = Scope()
        self.scopes.appendleft(scope)

    def push_scope(self, scope: Scope):
        self.scopes.appendleft(scope)

    def get_scope(self):
        return self.scopes[0]

    def pop_scope(self):
        self.scopes.popleft()

    def add_variable(self, var: Variable):
        self.scopes[0].add_variable(var)

    def get_variable(self, name: id):
        for scope in self.scopes:
            if variable := scope.get_variable(name):
                return variable

    def scope_var_exists(self, var_name: str):
        return self.scopes[0].var_exists(var_name)

    def context_var_exist(self, var_name: str):
        result = False
        for scope in self.scopes:
            if scope.var_exists(var_name):
                result = True
                break
        return result

    def peek_scope(self):
        pass
