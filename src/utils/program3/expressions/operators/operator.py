from typing import List

from src.exceptions import ValidationException
from src.utils.program3.node import Node


class Operator(Node):

    def __init__(self):
        self.oper = ""

    @staticmethod
    def validate_operator_types(operators: List) -> bool:
        if len(operators) > 0 and not all([isinstance(oper, Operator) for oper in operators]):
            raise ValidationException(f"All operator components should be of Operator datatype")
        return True

    def __str__(self):
        return self.oper

    def __repr__(self):
        return f"Operator(\"{self.oper}\")"
