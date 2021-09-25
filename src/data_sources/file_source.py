from .base_source import BaseSource
from src.utils.position import Position

from typing import TextIO, Optional

class FileSource(BaseSource):

    def __init__(self, file_obj: TextIO):

        self.reader = file_obj
        self.position = Position()
        self.read_char()

    # TODO: refactor these methods to the text_source class ???
    def read_char(self) -> Optional[str]:
        """
        :return: Exactly one char or None
        """
        char = self.reader.read(1)
        if char:
            self.advance_position(char)
            self.character = char
        else:
            self.character = -1

    def advance_position(self, char):
        if char == "\n":
            self.position.advance_line()
        else:
            self.position.advance_column()

    def get_char(self):
        return self.character

    def get_position(self):
        return self.position