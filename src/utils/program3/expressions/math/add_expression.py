from typing import List

from src.utils.visitor import Visitor
from src.utils.program3.expressions.expression import Expression
from src.utils.program3.expressions.math.arithmetic_expression import ArithmeticExpression
from src.utils.program3.expressions.operators.operator import Operator


class AddExpression(ArithmeticExpression):

    # PLUS AND MINUS

    def __init__(self, expressions: List[Expression], operators: List[Operator]):
        super().__init__(expressions, operators)
        self.expressions = expressions
        self.operators = operators

    def __repr__(self):
        operators_string = "[" + ", ".join([str(operator) for operator in self.operators]) + "]"
        return f"AddExpression(operator={operators_string}, {len(self.expressions)})"

    def accept(self, visitor: Visitor):
        visitor.visit_add_expression(self)
