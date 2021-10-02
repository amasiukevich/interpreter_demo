from src.utils.program3.expressions.expression import Expression
from src.utils.program3.expressions.math.unary_expression import UnaryExpression
from src.utils.program3.expressions.operators.negative_oper import NegativeOperator


class NegativeUnaryExpression(UnaryExpression):

    def __init__(self, expression: Expression):
        super().__init__(expression, NegativeOperator())
        self.expression = expression
        self.operator = NegativeOperator()

    def __repr__(self):
        return f"NegativeUnaryExpression()"
