from src.utils.visitor_old import Visitor
from src.utils.program3.expressions.expression import Expression
from src.utils.program3.statements.statement import Statement


class Return(Statement):

    def __init__(self, expression: Expression):
        self.expression = expression

    def __str__(self):
        if self.expression:
            string = f"return {self.expression};"
        else:
            string = f"return;"
        return string

    def __repr__(self):
        return "Return()"

    def accept(self, visitor: Visitor):
        visitor.visit_return(self)
