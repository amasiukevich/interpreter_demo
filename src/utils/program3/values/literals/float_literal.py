from src.utils.program3.values.literals.literal import Literal


class FloatLiteral(Literal):

    def __init__(self, value: float):

        # TODO: casting rules here

        if not isinstance(value, float):
            # TODO: custom exception here
            raise Exception("FloatLiteral can only be created using boolean value")
        self.value = value

    def __str__(self):
        return f"{self.value}"

    def __repr__(self):
        return f"FloatLiteral(value={self.value})"
