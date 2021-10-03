from src.exceptions.validation_exception import ValidationException
from src.utils.program3.expressions.operators.operator import Operator
from src.utils.program3.expressions.expression import Expression


class UnaryExpression(Expression):

    def __init__(self, expression: Expression, operator: Operator):

        if UnaryExpression.validate_operator(operator) and \
                UnaryExpression.validate_expression(expression):

            self.expression = expression
            self.operator = operator

    @staticmethod
    def validate_operator(operator: Operator) -> bool:

        if not operator or not isinstance(operator, Operator):
            raise ValidationException(
                "UnaryExpression object cannot be created without a proper operator"
            )
        return True

    @staticmethod
    def validate_expression(expression: Expression):

        if not expression or not isinstance(expression, Expression):
            raise ValidationException(
                "UnaryExpression object cannot be created without a proper expression"
            )
        return True

    def __str__(self):
        return f"{self.operator}({self.expression})"

    # repr is unique
