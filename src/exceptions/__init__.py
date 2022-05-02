from src.utils.token import Token
from src.utils.token_type import TokenType
from src.utils.position import Position


class RuntimeException(Exception):

    def __init__(self, message=""):
        super().__init__(message)
        self.message = message

    def get_message(self):
        return self.message


class ArithmeticException(Exception):

    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def get_message(self):
        return self.message

class ParsingException(Exception):

    def __init__(self, token: Token, ext_token_type: TokenType, message: str):

        self.token = token
        self.token_type = ext_token_type
        self.message = message or f"Expected {token.token_type}, got {ext_token_type} at {self.token.position}"
        super().__init__(message)

    def get_message(self):
        return f"ParsingException: {self.message}"


class PositionException(Exception):

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class ScanningException(Exception):

    def __init__(self, position: Position, message: str):
        self.position = position
        self.message = message
        self._message_string = f"ScanningException at position: {self.position}\n{self.message}"
        super().__init__(self._message_string)

    def get_message(self):
        return self._message_string

class ValidationException(Exception):

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
        self._message_string = f"ValidationException: {message}"

    def get_message(self):
        return self._message_string

class InterpretingException(Exception):

    def __init__(self, message):
        super().__init__(self)
        self.message = message
