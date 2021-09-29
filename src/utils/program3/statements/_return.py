from src.utils.program3.node import Node
from src.utils.program3.expressions.expression import Expression


class Return(Node):

    def __init__(self, expression: Expression):
        self.expression = expression

    def __str__(self):
        return f"return {self.expression};"

    def __repr__(self):
        return "Return()"
