from collections import deque
from typing import Optional, Union

from src.exceptions import RuntimeException
from src.utils.program3.values.value import Value
from src.utils.program3.variable import Variable
from src.utils.interpreter_utils.call_context import CallContext


class Environment:

    def __init__(self):
        self.value_stack = deque()
        self.call_stack = deque()
        self.is_returned = False

    def push_new_fcc(self):
        self.call_stack.append(CallContext())

    @staticmethod
    def is_empty_stack(stack):
        return len(stack) == 0

    def pop_fcc(self):
        if not Environment.is_empty_stack(self.call_stack):
            return self.call_stack.pop()

    def get_top_fcc(self) -> Optional[CallContext]:
        if not Environment.is_empty_stack(self.call_stack):
            return self.call_stack[-1]

    def push_value(self, value: Value):
        self.value_stack.append(value)

    def pop_value(self):
        if Environment.is_empty_stack(self.value_stack):
            return self.value_stack.pop()

    def get_variable(self, var_name: str) -> Optional[Variable]:
        variable = self.get_top_fcc.get_variable(var_name)
        if not variable:
            variable = self.global_scope.get_variable(var_name)
        # Search in global scope
        if not variable:
            # TODO: Custom exception here
            raise Exception(f"Cannot find variable {var_name}")

        return variable

    def get_is_returned(self):
        return self.is_returned

    def set_is_returned(self, is_returned):
        self.is_returned = is_returned

    def add_variable(self, var: Variable):
        self.get_top_fcc().add_variable(var)


class DummyEnvironment:

    # Enclosing environment is needed to traverse a chain of environments
    # TODO: Suggestion - wouldn't it be easier to implement it as a stack?
    def __init__(self, enclosing=None):
        self.values = {}
        self.enclosing = enclosing

    def define(self, name, value):
        """ Important! Assignment doesn't require a variable to be defined within the scope """
        self.values[name] = value

    def get_variable_or_function(self, name: str):

        if name in self.values.keys():
            return self.values.get(name)
        elif self.enclosing:
            return self.enclosing.get_variable_or_function(name)
        else:
            raise RuntimeException(message=f"Undefined variable: {name}.")
