from src.exceptions.validation_exception import ValidationException
from src.utils.program3.node import Node

from typing import List


class Expression(Node):

    @staticmethod
    def validate_expression_types(expressions: List) -> bool:
        if len(expressions) > 0 and not all([isinstance(expr, Expression) for expr in expressions]):
            raise ValidationException(f"All expression components should be of Expression datatype")
        return True
