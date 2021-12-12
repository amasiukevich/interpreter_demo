from typing import List

from src.exceptions import ValidationException
from src.utils.program3.block import Block
from src.utils.program3.expressions.expression import Expression
from src.utils.program3.statements.statement import Statement


class Conditional(Statement):

    def __init__(self, expressions: List[Expression], blocks: List[Block]):

        if Conditional.validate_expressions(expressions) and \
                Conditional.validate_blocks(blocks) and \
                Conditional.validate_matching(expressions, blocks):
            self.expressions = expressions
            self.blocks = blocks
            self.num_else_ifs = len(self.expressions) - 1 if len(self.expressions) >= 2 else 0

    @staticmethod
    def validate_expressions(expressions: List[Expression]) -> bool:
        is_valid = True
        if len(expressions) <= 0:
            raise ValidationException("Cannot parse Conditional without component expressions")

        if not all([isinstance(expression, Expression) for expression in expressions]):
            raise ValidationException("All of the expression components must be of Expression datatype")

        return is_valid

    @staticmethod
    def validate_blocks(blocks: List[Block]) -> bool:

        is_valid = True
        if len(blocks) <= 0:
            raise ValidationException("Cannot parse Conditional without component blocks")

        if not all([isinstance(block, Block) for block in blocks]):
            raise ValidationException("All of the block components must be of Block datatype")

        return is_valid

    @staticmethod
    def validate_matching(expressions: List[Expression], blocks: List[Block]) -> bool:
        is_valid = True
        # single if case
        if len(expressions) == len(blocks) != 1:
            raise ValidationException("Number of expressions equals number of blocks only in single if conditional")

        if len(blocks) - len(expressions) != 1 and len(blocks) != 1:
            raise ValidationException("Inconsistent number of blocks and expressions in conditional")
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
        return f"Conditional(num_else_ifs={self.num_else_ifs}, " \
               f"has_else={len(self.expressions) > 1})"

    # TODO: make fancy looking code including tabs with external visitor
