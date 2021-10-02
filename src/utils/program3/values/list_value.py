from src.utils.program3.values.value import Value
from src.utils.program3.expressions.expression import Expression

from typing import List


class ListValue(Value):

    def __init__(self, expressions: List[Expression] = []):

        if Expression.validate_expression_types(expressions):
            self.expressions = expressions

    def __str__(self):

        base_list_string = "["
        if len(self.expressions) > 0:
            base_list_string += ", ".join([f"{expr}" for expr in self.expressions])
        base_list_string += "]"

        return base_list_string

    def __repr__(self):
        return f"ListValue({len(self.expressions)})"
