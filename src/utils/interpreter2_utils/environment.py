from collections import deque
from .call_utils import AbcFunction
from .call_context import CallContext
from .scope import Scope
from src.utils.program3.variable import Variable
from src.utils.program3.values.value import Value


class Environment:

    def __init__(self):
        # Stacks
        self.values = deque()
        self.call_contexts = deque()

        self.push_new_call_context()

        self.returned_with_value = False
        self.returned = False

    def push_new_call_context(self):
        self.call_contexts.appendleft(CallContext())

    def push_new_scope(self):
        self.call_contexts[0].push_scope(Scope())

    def pop_scope(self):
        self.call_contexts[0].pop_scope()

    def pop_call_context(self):
        self.call_contexts.popleft()

    def add_variable(self, var: Variable):
        self.call_contexts[0].add_variable(var)

    # TODO: for classes, objects and stuff
    # TODO: maybe pass some context
    def add_fancy_variable(self, var: Variable, call_context: CallContext):
        needed_idx = self.call_contexts.index(call_context)
        self.call_contexts[needed_idx].add_variable()

    def get_variable(self, name: str):
        return self.call_contexts[0].get_variable(name)

    # TODO: for classes, objects and stuff
    # TODO: maybe pass some context
    def get_fancy_variable(self):
        pass

    def push_value(self, value: Value):
        self.values.appendleft(value)

    def pop_value(self):
        return self.values.popleft()

    # TODO: if broken/returned/continued there...

    def is_returned_with_value(self):
        return self.returned_with_value

    def is_returned(self):
        return self.returned

    def set_returned(self, val: bool):
        self.returned = val

    def set_returned_with_value(self, val: bool):
        self.returned_with_value = val
