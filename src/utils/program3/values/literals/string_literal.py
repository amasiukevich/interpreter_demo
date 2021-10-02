from src.utils.program3.values.literals.literal import Literal


class StringLiteral(Literal):

    def __init__(self, value: str):

        # TODO: casting rules here

        if not isinstance(value, str):
            # TODO: custom exception here
            raise Exception("StringLiteral can only be created using string value")
        self.value = value

    def __str__(self):
        return f"\"{self.value}\""

    def __repr__(self):
        return f"StringLiteral(value=\"{self.value}\")"
