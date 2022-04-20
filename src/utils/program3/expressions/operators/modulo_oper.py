from src.utils.program3.expressions.operators.operator import Operator
from src.utils.visitor import Visitor


class ModuloOperator(Operator):

    def __init__(self):
        self.oper = "%"

    def __eq__(self, other):
        return type(self) == type(other)

    def accept(self, visitor: Visitor):
        visitor.visit_modulo_oper(self)
