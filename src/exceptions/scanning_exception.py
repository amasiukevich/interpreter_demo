from src.utils.position import Position


class ScanningException(Exception):

    def __init__(self, position: Position, message: str):
        self.position = position
        self.message = message
        self._message_string = f"ScanningException at position: {self.position}\n{self.message}"
        super().__init__(self._message_string)

    def get_message(self):
        return self._message_string
