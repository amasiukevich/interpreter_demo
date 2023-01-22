from src.utils.program3.expressions.expression import Expression
from src.utils.program3.values.value import Value
from src.utils.interpreter_utils.call_utils import AbcFunction
from src.utils.visitor import Visitor

from typing import Union


class Variable(Expression):

    def __init__(self, name: str, value: Union[Value, AbcFunction] = None):
        self.name = name
        self.value = value

    def set_value(self, value):
        self.value = value

    def accept(self, visitor: Visitor):
        visitor.visit_variable(self)
