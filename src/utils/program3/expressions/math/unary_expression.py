from src.exceptions import ValidationException
from src.utils.program3.expressions.expression import Expression
from src.utils.program3.values.value import Value
from src.utils.program3.expressions.operators.operator import Operator
from src.utils.program3.expressions.operators.negative_oper import NegativeOperator
from src.utils.program3.expressions.operators.not_oper import NotOperator
from src.utils.visitor import Visitor


class UnaryExpression(Expression):

    def __init__(self, expression: Expression, operator: Operator=None):

        if UnaryExpression.validate_operator(operator) and \
            Expression.validate_expression_types([expression]):
            self.expression = expression
            self.operator = operator

    @staticmethod
    def validate_operator(operator: Operator=None):
        if not (
            operator is None or
            Operator.validate_operator_types([operator]) or
            isinstance(operator, NegativeOperator) or isinstance(operator, NotOperator)
        ):
            raise ValidationException(f"UnaryExpression object cannot be created without a proper operator")

        return True

    def __str__(self):

        components = []
        if self.operator:
            components.append(f"{self.operator}")
        if isinstance(self.expression, Value):
            components.append(f"{self.expression}")
        elif isinstance(self.expression, Expression):
            components.append(f"({self.expression})")

        return "".join(components)

    def __repr__(self):
        return f"UnaryExpression(has_operator={bool(self.operator)})"

    def accept(self, visitor: Visitor):
        visitor.visit_unary_expression(self)
