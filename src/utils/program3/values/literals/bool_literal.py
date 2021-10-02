from src.utils.program3.values.literals.literal import Literal


class BoolLiteral(Literal):

    def __init__(self, value: bool):

        # TODO: casting rules here

        if value not in [True, False]:
            # TODO: custom exception here
            raise Exception("BoolLiteral can only be created using boolean value")
        self.value = value

    def __str__(self):
        return f"{self.value}"

    def __repr__(self):
        return f"BoolLiteral(value={self.value}"
