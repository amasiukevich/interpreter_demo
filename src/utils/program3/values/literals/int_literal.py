from src.exceptions import ValidationException
from src.utils.program3.values.literals.literal import Literal
from src.utils.visitor import Visitor


class IntLiteral(Literal):

    def __init__(self, value: int):

        # TODO: casting rules here

        if not isinstance(value, int):
            raise ValidationException("IntLiteral can only be created using integer value")
        self.value = value

    def __str__(self):
        return f"{self.value}"

    def __repr__(self):
        return f"IntLiteral(value={self.value})"

    def accept(self, visitor: Visitor):
        return visitor.visit_literal(self)
