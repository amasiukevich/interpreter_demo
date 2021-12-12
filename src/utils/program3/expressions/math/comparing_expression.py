from typing import List

from src.exceptions import ValidationException
from src.utils.program3.expressions.expression import Expression
from src.utils.program3.expressions.operators.operator import Operator


class ComparingExpression(Expression):

    def __init__(self, expressions: List[Expression], operator: Operator):

        if Expression.validate_expression_types(expressions) and \
            Operator.validate_operator_types([operator]) and \
            ComparingExpression.validate_comparing_expr(expressions):

            self.expressions = expressions
            self.operator = operator

    @staticmethod
    def validate_comparing_expr(expressions) -> bool:

        if len(expressions) != 2:
            raise ValidationException(f"Inconsistent number of expression components")
        return True

    def __str__(self):
        symbol = self.operator.oper
        return f"{symbol}".join([str(expr) for expr in self.expressions])
