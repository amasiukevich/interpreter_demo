from .base_source import BaseSource
from src.utils.position import Position

from typing import TextIO, Optional

class StringSource(BaseSource):

    def __init__(self, string_stream: TextIO):

        self.reader = string_stream
        self.position = Position()
        self.character = self.read_char

    # TODO: refactor this methods to the "text_source" class ???
    def read_char(self) -> Optional[str]:
        """
        :return: Exactly on char or None
        """
        char = self.reader.read(1)
        if char:
            self.advance_position(char)

        return char

    @staticmethod
    def advance_position(self, char):

        if char == "\n":
            self.position.advance_line()
        else:
            self.position.advance_column()

    def get_curr_char(self):
        return self.character