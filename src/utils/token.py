from . import TokenType, Position


class Token:

    SPECIAL_CHARS = []
    MAX_IDENTIFIER_LENGTH = 120
    MAX_NUMBER = 2 ** 32

    def __init__(self, token_type: TokenType, position: Position, value: str=None):

        self.token_type = token_type
        self.position = position
        self.value = value

    def get_token_type(self):
        return self.token_type
    
    def __eq__(self, other):
        if not isinstance(other, Token):
            return False
        else:
            return self.token_type == other.token_type and self.position == other.position and self.value == other.value

    def __str__(self):
        return f"Type: {self.token_type}\n" \
               f"Position: {self.position}\n" \
               f"Value: {self.value}\n"

    def __repr__(self):
        return self.__str__()