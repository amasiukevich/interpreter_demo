from typing import List

from src.utils.program3.expressions.expression import Expression
from src.utils.program3.expressions.math.comparing_expression import ComparingExpression
from src.utils.program3.expressions.operators.operator import Operator
from src.utils.visitor import Visitor


class RelationExpression(ComparingExpression):

    # Greater, Greater-Equal, Less, Less-Equal

    def __init__(self, expressions: List[Expression], operator: Operator):
        super().__init__(expressions, operator)
        self.expressions = expressions
        self.operator = operator

    def __repr__(self):
        return f"RelationExpression(operator={self.operator}, {len(self.expressions)})"

    def accept(self, visitor: Visitor):
        return visitor.visit_rel_expression(self)
