from src.utils.program3.expressions.expression import Expression
from src.utils.program3.expressions.math.unary_expression import UnaryExpression
from src.utils.program3.expressions.operators.not_oper import NotOperator


class NotUnaryExpression(UnaryExpression):

    def __init__(self, expression: Expression):
        super().__init__(expression, NotOperator())
        self.expression = expression
        self.operator = NotOperator()

    def __repr__(self):
        return f"NotUnaryExpression()"
