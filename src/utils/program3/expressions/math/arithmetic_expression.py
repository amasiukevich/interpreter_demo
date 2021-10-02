from src.utils.program3.expressions.expression import Expression
from src.utils.program3.expressions.operators.operator import Operator

from typing import List


class ArithmeticExpression(Expression):

    def __init__(self, expressions: List[Expression], operators: List[Operator]):

        if Expression.validate_expression_types(expressions) and \
            Operator.validate_operator_types(operators) and \
                ArithmeticExpression.validate_differs_in_one(expressions, operators):

            self.expressions = expressions
            self.operators = operators

    @staticmethod
    def validate_differs_in_one(expressions, operators):
        if len(expressions) - len(operators) != 1:
            # TODO: Custom exception here
            raise Exception(f"Number of exception components should be greater than number of operators by exactly 1")
        return True

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
