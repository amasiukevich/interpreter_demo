from typing import List

from src.utils.program3.expressions.expression import Expression
from src.utils.program3.expressions.math.logical_expression import LogicalExpression
from src.utils.program3.expressions.operators.and_oper import AndOperator


class AndExpression(LogicalExpression):

    def __init__(self, expressions: List[Expression]):
        super().__init__(expressions, operator=AndOperator())
        self.operator = "&&"
        self.expressions = expressions

    def __repr__(self):
        return f"AndExpression(n_expressions={len(self.expressions)})"
