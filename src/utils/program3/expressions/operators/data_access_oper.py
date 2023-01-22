from src.utils.program3.expressions.operators.operator import Operator
from src.utils.visitor import Visitor


class DataAccessOperator(Operator):

    def __init__(self):
        self.oper = "."

    def __eq__(self, other):
        return type(self) == type(other)

    def accept(self, visitor: Visitor):
        visitor.visit_data_access_oper(self)
