from src.utils.program3.node import Node

from typing import List


class Operator(Node):

    def __init__(self):
        self.oper = ""

    @staticmethod
    def validate_operator_types(operators: List) -> bool:
        if len(operators) > 0 and not all([isinstance(oper, Operator) for oper in operators]):
            # TODO: Custom exception here
            raise Exception(f"All operator components should be of Operator datatype")
        return True

    def __str__(self):
        return self.oper

    def __repr__(self):
        return f"Operator(\"{self.oper}\")"