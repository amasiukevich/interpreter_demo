from src.utils.program3.block import Block
from src.utils.program3.expressions.expression import Expression
from src.utils.program3.statements.loop import Loop


class ForeachLoop(Loop):

    def __init__(self, identifier: str, expression: Expression, block: Block):
        self.identifier = identifier
        self.expression = expression
        self.block = block

    def __str__(self):
        return f"foreach {self.identifier} in {self.expression} {self.block}"

    def __repr__(self):
        return f"ForeachLoop(identifier={self.identifier}, " \
               f"expression={self.expression}), " \
               f"block={self.block})"

    # TODO: Fancy tostring using visitor