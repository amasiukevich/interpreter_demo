from src.utils.program3.expressions.operators.operator import Operator
from src.utils.program3.expressions.expression import Expression

from typing import Optional


class UnaryExpression(Expression):

    def __init__(self, expression: Expression, operator: Optional[Operator]):

        self.expression = expression
        if operator:
            self.operator = operator

    # TODO: Make fancy representation of the expression
    def __str__(self):
        pass

    # TODO: Make it good for testing
    def __repr__(self):
        pass
