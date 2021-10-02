from src.utils.program3.expressions.expression import Expression
from src.utils.program3.expressions.operators.operator import Operator


from typing import List


class LogicalExpression(Expression):

    def __init__(self, expressions: List[Expression], operator: Operator):

        if Expression.validate_expression_types(expressions):
            self.expressions = expressions
            self.operator = operator

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
