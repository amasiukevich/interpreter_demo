from src.utils.program3.statements.statement import Statement
from src.utils.program3.expressions.expression import Expression


class Reflect(Statement):

    def __init__(self, is_recursive: bool, expression: Expression):
        self.is_recursive = is_recursive
        self.expression = expression

    def __str__(self):

        reflect_string = "reflect "
        if self.is_recursive:
            reflect_string += "recursive "
        reflect_string += f"{self.expression};"

        return reflect_string

    def __repr__(self):
        return f"Reflect(is_recursive={self.is_recursive}, expression={self.expression})"

    def __eq__(self, other):
        return self.is_recursive == other.is_recursive
