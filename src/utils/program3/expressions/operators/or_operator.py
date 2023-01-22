from src.utils.program3.expressions.operators.operator import Operator
from src.utils.visitor import Visitor


class OrOperator(Operator):

    def __init__(self):
        super().__init__()
        self.oper = "||"

    def __eq__(self, other):
        return type(self) == type(other)

    def accept(self, visitor: Visitor, left_value=None, right_value=None):
        return visitor.visit_or_oper(self)
