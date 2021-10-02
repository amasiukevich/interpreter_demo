from src.utils.program3.expressions.operators.operator import Operator
from src.utils.program3.expressions.expression import Expression

from typing import Optional


class UnaryExpression(Expression):

    def __init__(self, expression: Expression, operator: Optional[Operator]):

        self.expression = expression
        if operator:
            self.operator = operator


    def __str__(self):
        return f"{self.operator}({self.expression})"

    # repr is unique