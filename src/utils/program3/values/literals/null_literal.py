from src.utils.program3.values.literals.literal import Literal
from src.utils.visitor import Visitor


class NullLiteral(Literal):

    def __init__(self):
        self.value = None

    def __str__(self):
        return f"{self.value}"

    def __repr__(self):
        return f"NullLiteral()"

    def accept(self, visitor: Visitor):
        return visitor.visit_literal(self)

