from src.utils.program3.node import Node
from src.utils.program3.expressions.expression import Expression


class Argument(Node):

    def __init__(self, is_by_ref: bool, expression: Expression):

        if not isinstance(expression, Expression):
            raise Exception("An expression in argument must be of expression datatype")

        self.expression = expression
        self.is_by_ref = is_by_ref

    def __str__(self):

        argument_string = ""
        if self.is_by_ref:
            argument_string += "by_ref "

        argument_string += f"{self.expression}"
        return argument_string

    def __repr__(self):
        return f"Argument(by_ref={self.is_by_ref})"

    # TODO: Add fancy tabs with external visitor

    # TODO: Implement visiting logic with "by_ref"
