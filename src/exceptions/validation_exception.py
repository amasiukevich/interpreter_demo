class ValidationException(Exception):

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
        self._message_string = f"ValidationException: {message}"

    def get_message(self):
        return self._message_string