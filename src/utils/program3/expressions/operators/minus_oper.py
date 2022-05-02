from src.utils.program3.expressions.operators.operator import Operator
from src.utils.visitor import Visitor


class MinusOperator(Operator):

    def __init__(self):
        self.oper = "-"

    def __eq__(self, other):
        return type(self) == type(other)

    def accept(self, visitor: Visitor, left_value, right_value):
        return visitor.visit_minus_oper(self, left_value, right_value)
