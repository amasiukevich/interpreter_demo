from src.exceptions.position_exception import PositionException

class Position:

    def __init__(self, line=1, column=0):

        if line <= 0:
            raise PositionException("Line cannot be less than 1")

        if column < 0:
            raise PositionException("Column cannot be less than 0")


        self.line = line
        self.column = column

    def advance_line(self):
        self.line += 1
        self.column = 0

    def advance_column(self):
        self.column += 1

    def __str__(self):
        return f"line: {self.line}, column: {self.column}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):

        if not isinstance(other, Position):
            raise PositionException(f"Cannot compare {type(self).__name__} and {type(other).__name__}")
        else:
            return self.line == other.line and self.column == other.column

    def clone(self):
        return Position(line=self.line, column=self.column)
