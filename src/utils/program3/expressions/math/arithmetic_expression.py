from src.utils.program3.expressions.expression import Expression
from src.utils.program3.expressions.operators.operator import Operator

from typing import List


class ArithmeticExpression(Expression):

    def __init__(self, expressions: List[Expression], operators: List[Operator]):

        if self.validate_arithmetic_expression(expressions, operators):
            self.expressions = expressions
            self.operator = operators

    @staticmethod
    def validate_arithmetic_expression(expressions: List[Expression], operators: List[Operator]) -> bool:

        is_valid = True
        if len(expressions) > 0 and not all([isinstance(expr, Expression) for expr in expressions]):
            # TODO: Custom exception here
            raise Exception("All expression components must be of Expression datatype")

        if len(operators) > 0 and not all([isinstance(expr, Expression) for expr in expressions]):
            # TODO: Custom exception hera
            raise Exception("All operators should be of Operator datatype")

        if len(expressions) - len(operators) != 1:
            # TODO: Custom exception here
            raise Exception("Number of exception components should be greater than number of operators by 1 exactly")

        return is_valid

    def __str__(self):

        arithm_expr_string = ""
        if len(self.expressions) == 1:
            arithm_expr_string = f"{self.expressions[0]}"
        elif len(self.expressions) > 1:
            arithm_expr_string += f"({self.expressions[0]}"
            for i in range(1, len(self.expressions)):
                arithm_expr_string += f" {self.operators[i - 1]} "
                arithm_expr_string += f"{self.expressions[i]}"
            arithm_expr_string += ")"

        return arithm_expr_string

    # repr is custom
