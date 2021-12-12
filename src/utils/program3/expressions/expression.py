from typing import List

from src.exceptions import ValidationException
from src.utils.program3.node import Node


class Expression(Node):

    @staticmethod
    def validate_expression_types(expressions: List) -> bool:
        if len(expressions) > 0 and not all([isinstance(expr, Expression) for expr in expressions]):
            raise ValidationException(f"All expression components should be of Expression datatype")
        return True
