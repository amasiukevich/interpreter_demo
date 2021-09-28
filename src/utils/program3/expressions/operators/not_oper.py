from src.utils.program3.expressions.operators.operator import Operator


class NotOperator(Operator):

    def __init__(self):
        self.oper = "!"

    def __eq__(self, other):
        return type(self) == type(other)
