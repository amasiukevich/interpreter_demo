from src.utils.position import Position


class ScanningException(Exception):

    def __init__(self, position: Position, message: str):
        self.position = position
        self.message = message
        super().__init__(message)

    # TODO: Add magic methods here
    def __str__(self):
        pass

    def __repr__(self):
        pass