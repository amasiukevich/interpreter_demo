from src.utils.program3.statements.statement import Statement
from src.utils.program3.expressions.expression import Expression
from src.utils.program3.block import Block

from typing import List


class Conditional(Statement):

    def __init__(self, expressions: List[Expression], blocks: List[Block]):

        if Conditional.validate_expressions(expressions) and \
                Conditional.validate_blocks(blocks) and \
                Conditional.validate_matching(expressions, blocks):
            self.expressions = expressions
            self.blocks = blocks
            self.num_else_ifs = len(self.expressions) - 1 if len(self.expressions) > 2 else 0

    @staticmethod
    def validate_expressions(expressions: List[Expression]) -> bool:
        is_valid = True
        if len(expressions) <= 0:
            # TODO: Custom exception here
            raise Exception("Cannot parse Conditional without component expressions")

        if not all([isinstance(expression, Expression) for expression in expressions]):
            # TODO: Custom exception here
            raise Exception("All of the expression components must be of Expression datatype")

        return is_valid

    @staticmethod
    def validate_blocks(blocks: List[Block]) -> bool:

        is_valid = True
        if len(blocks) <= 0:
            # TODO: custom exception here
            raise Exception("Cannot parse Conditional without component blocks")

        if not all([isinstance(block, Block) for block in blocks]):
            # TODO: custom exception here
            raise Exception("All of the block components must be of Block datatype")

        return is_valid

    @staticmethod
    def validate_matching(expressions: List[Expression], blocks: List[Block]) -> bool:
        is_valid = True
        # single if case
        if len(expressions) == len(blocks) != 1:
            # TODO: custom exception here
            raise Exception("Number of expressions equals number of blocks only in single if conditional")
        elif len(blocks) - len(expressions) != 1:
            # TODO: custom exception here
            raise Exception("Inconsistent number of blocks and expressions in conditional")
        return is_valid

    def __str__(self):

        base_conditional_string = f"if {self.expressions[0]} {self.blocks[0]}"
        if self.num_else_ifs > 0:
            for i in range(self.num_else_ifs):
                base_conditional_string += f" else if {self.expressions[i + 1]} {self.blocks[i + 1]}"

        if len(self.blocks) > 1:
            base_conditional_string += f" else {self.blocks[-1]}"

        return base_conditional_string

    def __repr__(self):

        return f"Conditional(has_if={len(self.expressions) >= 1}, " \
               f"num_else_ifs={self.num_else_ifs}, " \
               f"has_else={len(self.expressions) > 1})"

    # TODO: make fancy looking code including tabs with external visitor
