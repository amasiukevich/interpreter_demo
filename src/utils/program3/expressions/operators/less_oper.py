from src.utils.program3.expressions.operators.operator import Operator


class LessOperator(Operator):

    def __init__(self):
        self.oper = "<"

    def __eq__(self, other):
        return type(self) == type(other)
