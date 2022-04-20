from abc import ABC
from collections.abc import Callable

from src.utils.visitor import Visitor
from src.utils.program3.functions.parameters import Parameters


class AbcFunction(ABC):
    pass


class NativeFunction(AbcFunction):

    def __init__(self, arity: int, call_func: Callable = None):
        self.call_func = call_func
        self.arity = arity

    def accept(self, visitor: Visitor):
        visitor.visit_native_function(self)
