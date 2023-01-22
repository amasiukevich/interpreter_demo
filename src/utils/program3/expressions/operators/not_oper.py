from src.utils.program3.expressions.operators.operator import Operator
from src.utils.visitor import Visitor


class NotOperator(Operator):

    def __init__(self):
        self.oper = "!"

    def __eq__(self, other):
        return type(self) == type(other)

    def accept(self, visitor: Visitor, value):
        return visitor.visit_not_oper(self, value)
