from typing import List

from src.utils.program3.expressions.expression import Expression
from src.utils.program3.expressions.math.logical_expression import LogicalExpression
from src.utils.program3.expressions.operators.or_operator import OrOperator
from src.utils.visitor import Visitor


class OrExpression(LogicalExpression):

    def __init__(self, expressions: List[Expression]):
        super().__init__(expressions, operator=OrOperator())
        self.operator = "||"
        self.expressions = expressions

    def __repr__(self):
        return f"OrExpression(n_expressions={len(self.expressions)})"

    def accept(self, visitor: Visitor):
        return visitor.visit_or_expression(self)
