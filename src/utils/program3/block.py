from typing import List

from src.exceptions import ValidationException
from src.utils.program3.node import Node
from src.utils.program3.statements.statement import Statement
from src.utils.visitor import Visitor


class Block(Node):

    def __init__(self, statements: List[Statement] = []):

        if len(statements) > 0 and not all([isinstance(statement, Statement) for statement in statements]):
            raise ValidationException("All component statements in block should be of Statement datatype")

        self.statements = statements

    def get_statements(self):
        return self.statements

    def __eq__(self, other):
        return len(self.statements) == len(other.statements)

    def __str__(self):

        block_string = "{\n"
        for statement in self.statements:
            block_string += f"\t{statement}\n"

        block_string += "}"
        return block_string

    def __repr__(self):
        return f"Block(n_statements={len(self.statements)})"

    def accept(self, visitor: Visitor):
        visitor.visit_block(self)

    # TODO: Beautify __str__ after visiting
