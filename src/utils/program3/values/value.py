from abc import ABCMeta

from src.utils.program3.expressions.expression import Expression
from src.utils.visitor_old import Visitor


class Value(Expression, metaclass=ABCMeta):
    pass
    # def accept(self, visitor: Visitor):
    #     visitor.visit_value(self)
