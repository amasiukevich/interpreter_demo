from src.utils.program3.expressions.math.add_expression import AddExpression
from src.utils.program3.node import Node


class NoCallValueGetter(Node):

    def __init__(self, identifier: str, slicing_expr: AddExpression):
        self.identifier = identifier
        self.slicing_expr = slicing_expr

    def __str__(self):
        no_call_string = f"{self.identifier}"
        if self.slicing_expr is not None:
            no_call_string += f"[{self.slicing_expr}]"
        return no_call_string

    def __repr__(self):
        return f"NoCallValueGetter(identifier=\"{self.identifier}\")"
