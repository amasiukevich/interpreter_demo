from src.utils.program3.statements.statement import Statement
from src.utils.program3.expressions.expression import Expression


class Return(Statement):

    def __init__(self, expression: Expression):
        self.expression = expression

    def __str__(self):
        return f"return {self.expression};"

    def __repr__(self):
        return "Return()"
