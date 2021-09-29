from src.utils.program3.expressions.math.logical_expression import LogicalExpression
from src.utils.program3.expressions.expression import Expression

from typing import List


class AndExpression(LogicalExpression):

    def __init__(self, expressions: List[Expression]):

        if LogicalExpression.validate_logical_expression(expressions):
            self.operator = "&&"
            self.expressions = expressions

    def __repr__(self):
        return f"AndExpression({len(self.expressions)})"
