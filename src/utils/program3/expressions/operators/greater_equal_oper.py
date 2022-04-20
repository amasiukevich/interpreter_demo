from src.utils.program3.expressions.operators.operator import Operator
from src.utils.visitor import Visitor


class GreaterEqualOperator(Operator):

    def __init__(self):
        super().__init__()
        self.oper = ">="

    def __eq__(self, other):
        return type(self) == type(other)

    def accept(self, visitor: Visitor):
        visitor.visit_greater_equal_oper(self)
