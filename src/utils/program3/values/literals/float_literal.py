from src.exceptions import ValidationException
from src.utils.program3.values.literals.literal import Literal


class FloatLiteral(Literal):

    def __init__(self, value: float):

        # TODO: casting rules here

        if not isinstance(value, float):
            raise ValidationException("FloatLiteral can only be created using float value")
        self.value = value

    def __str__(self):
        return f"{self.value}"

    def __repr__(self):
        return f"FloatLiteral(value={self.value})"
