from collections import deque
from .call_utils import AbcFunction
from .call_context import CallContext
from .scope import Scope
from src.utils.program3.variable import Variable
from src.utils.program3.values.value import Value
from .call_utils import NativeFunction
from ..program3.values.literals.null_literal import NullLiteral


class Environment:

    def __init__(self):
        # Stacks
        self.values = deque()
        self.call_contexts = deque()

        self.push_new_call_context()

        self.returned = (False, None)

        self.set_native_functions()

    def set_native_functions(self):
        native_print = NativeFunction(arity=1, call_func=print)
        self.add_variable(Variable(name='print', value=native_print))

    def push_new_call_context(self, scope=None):
        self.call_contexts.appendleft(CallContext(scope))
        self.set_native_functions()

    def push_scope(self, scope=None):
        if not scope:
            scope = Scope()
        self.call_contexts[0].push_scope(scope)

    def pop_scope(self):
        self.call_contexts[0].pop_scope()

    def pop_call_context(self):
        self.call_contexts.popleft()

    def add_variable(self, var: Variable):
        self.call_contexts[0].add_variable(var)

    def get_variable(self, name: str):
        return self.call_contexts[0].get_variable(name)

    def push_value(self, value: Value):
        self.values.appendleft(value)

    def pop_value(self):
        return self.values.popleft()

    def set_returned(self, fact, value=None):
        self.returned = (fact, value)

    def reset_returned(self):
        self.set_returned(fact=False, value=None)

    def get_returned(self):
        return self.returned

    def release_scopes(self, n_scopes: int):
        for i in range(n_scopes):
            self.pop_scope()
