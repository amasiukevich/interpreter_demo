from src.utils.program3.expressions.expression import Expression
from src.utils.program3.expressions.operators.operator import Operator

from typing import List


class LogicalExpression(Expression):

    def __init__(self, expressions: List[Expression], operator: Operator):
        self.expressions = expressions
        self.operator = operator

    @staticmethod
    def validate_logical_expression(expressions: List[Expression]) -> bool:

        is_valid = True
        if len(expressions) > 0 and not all([isinstance(expr, Expression) for expr in expressions]):
            # TODO: Custom exception here
            raise Exception("All component elements in logical expression should be of Expression datatype")

        return is_valid

    def __str__(self):

        logic_expr_string = ""
        if len(self.expressions) > 0:
            logic_expr_string += "("
            logic_expr_string += f"{self.expressions[0]}"
            for i in range(1, len(self.expressions)):
                logic_expr_string += f" {self.operator} "
                logic_expr_string += f"{self.expressions[i]}"
            logic_expr_string += ")"

        return logic_expr_string

    # __repr__ is custom for every subclass
