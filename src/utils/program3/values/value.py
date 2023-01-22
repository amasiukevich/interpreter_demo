from abc import ABCMeta

from src.utils.program3.expressions.expression import Expression
from src.utils.visitor import Visitor

# TODO: Do we need value???
class Value(Expression):
    pass
    # def accept(self, visitor: Visitor):
    #     visitor.visit_value(self)
