from src.utils.program3.statements.loop import Loop
from src.utils.program3.expressions.expression import Expression
from src.utils.program3.block import Block


class WhileLoop(Loop):

    def __init__(self, expression: Expression, block: Block):
        self.expression = expression
        self.block = block

    def __str__(self):
        return f"while {self.expression} {self.block}"

    def __repr__(self):
        return f"WhileLoop(expression={self.expression}, block={self.block})"
