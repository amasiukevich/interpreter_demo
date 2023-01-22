from typing import List

from src.utils.visitor import Visitor
from src.utils.program3.expressions.expression import Expression
from src.utils.program3.expressions.operators.operator import Operator


class LogicalExpression(Expression):

    def __init__(self, expressions: List[Expression], operator: Operator):

        if Expression.validate_expression_types(expressions):
            self.expressions = expressions
            self.operator = operator

    def get_num_expressions(self):
        return len(self.expressions)

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

    def accept(self, visitor: Visitor):
        pass

    # __repr__ is custom for every subclass
