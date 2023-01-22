from typing import TextIO, Optional

from src.utils.position import Position
from .base_source import BaseSource


class StringSource(BaseSource):

    def __init__(self, string_stream: TextIO):

        self.reader = string_stream
        self.position = Position()
        self.read_char()

    # TODO: refactor this methods to the "text_source" class ???
    def read_char(self) -> Optional[str]:
        """
        :return: Exactly on char or None
        """
        char = self.reader.read(1)
        if char:
            self.advance_position(char)
            self.character = char
        else:
            self.character = -1

    def advance_position(self, char):

        if char in ["\036", "\025"]:

            self.position.advance_line()

        elif char == "\n":

            copied_ptr = self.reader.tell()
            self.reader.seek(copied_ptr)

            new_char = self.reader.read(1)
            self.position.advance_line()
            if new_char != "\r":
                self.reader.seek(copied_ptr)

        elif char == "\r":

            copied_ptr = self.reader.tell()
            self.reader.seek(copied_ptr)
            new_char = self.reader.read(1)
            self.position.advance_line()

            if new_char == "\n":
                self.reader.seek(copied_ptr)
        else:
            self.position.advance_column()

    def get_char(self):
        return self.character

    def get_position(self):
        return self.position