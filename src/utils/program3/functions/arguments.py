from typing import List

from src.utils.program3.node import Node
from src.utils.program3.expressions.expression import Expression


class Arguments(Node):

    def __init__(self, arguments: List[Expression]=[]):
        self.arguments = arguments

    def __str__(self):
        return ", ".join([str(argument) for argument in self.arguments])

    def __repr__(self):
        return f"Arguments(n_args={len(self.arguments)})"
