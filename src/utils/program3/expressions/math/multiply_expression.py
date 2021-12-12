from src.utils.program3.expressions.expression import Expression
from src.utils.program3.expressions.math.arithmetic_expression import ArithmeticExpression
from src.utils.program3.expressions.operators.operator import Operator

from typing import List


class MultiplyExpression(ArithmeticExpression):

    # MULTIPLY, DIVIDE AND MODULO

    def __init__(self, expressions: List[Expression], operators: List[Operator]):
        super().__init__(expressions, operators)

        self.expressions = expressions
        self.operator = operators

    def __repr__(self):
        operators_string = "[" + ", ".join([str(operator) for operator in self.operators]) + "]"
        return f"MultiplyExpression(operators={operators_string}, {len(self.expressions)})"
