from abc import ABC
from collections.abc import Callable
from typing import Optional, List

from src.utils.program3.values.literals.null_literal import NullLiteral
from src.utils.visitor import Visitor
from src.utils.program3.functions.parameters import Parameters


class AbcFunction(ABC):

    def __init__(self, return_value: Optional=None):
        self.return_value = return_value


class NativeFunction(AbcFunction):

    def __init__(self, arity: int, call_func: Callable = None, return_value: Optional[NullLiteral]=None):
        super().__init__(return_value)
        self.call_func = call_func
        self.arity = arity

    def accept(self, visitor: Visitor, evaluated_args: List):
        visitor.visit_native_function(self, evaluated_args)