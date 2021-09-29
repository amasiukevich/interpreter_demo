from src.utils.program3.expressions.math.arithmetic_expression import ArithmeticExpression
from src.utils.program3.expressions.expression import Expression
from src.utils.program3.expressions.operators.operator import Operator
from typing import List


class EqualityExpression(ArithmeticExpression):

    # Equal and Not equal

    def __init__(self, expressions: List[Expression], operators: List[Operator]):

        if ArithmeticExpression.validate_arithmetic_expression(expressions, operators):

            self.expressions = expressions
            self.operators = operators

    def __repr__(self):

        # TODO: Some error there
        operators_string = "[" + ", ".join([str(oper) for oper in self.operators]) + "]"
        return f"EqualityExpression(operators={operators_string}, {len(self.expressions)})"
