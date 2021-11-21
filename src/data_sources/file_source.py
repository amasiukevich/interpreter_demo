from src.utils import Position

from . import *
from typing import TextIO


class FileSource(BaseSource):

    def __init__(self, file_obj: TextIO):
        super().__init__()
        self.reader = file_obj
        self.position = Position()
        self.curr_char_line = []
        self.read_char()


    # TODO: refactor these methods to the text_source class ???
    def read_char(self) -> None:
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
            self.curr_char_line = []
        else:
            self.position.advance_column()
            self.curr_char_line.append(char)

    def get_char(self):
        return self.character

    def get_position(self):
        return self.position

    def get_line(self):

        # TODO: Think about the edge cases there (current char is the end of the string)
        # copy the current position in file
        copied_ptr = self.reader.tell()

        while self.character not in ["\n", -1]:
            self.character = self.reader.read(1)
            self.curr_char_line.append(self.character)

        line = "".join(self.curr_char_line)
        self.reader.seek(copied_ptr, 0)

        return line
