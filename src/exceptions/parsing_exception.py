from src.utils.token import Token
from src.utils.token_type import TokenType


class ParsingException(Exception):

    def __init__(self, token: Token, ext_token_type: TokenType, message: str):

        self.token = token
        self.token_type = ext_token_type
        self.message = message or f"Expected {token.token_type}, got {ext_token_type} at {self.token.position}"
        super().__init__(message)

    def get_message(self):
        return f"ParsingException: {self.message}"
