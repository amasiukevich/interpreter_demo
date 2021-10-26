from typing import List, Optional, Union

from src.utils.program3.node import Node
from src.utils.program3.functions.function import Function


class ClassBlock(Node):

    def __init__(self, methods: List[Function]=[]):
        self.methods = methods

    @staticmethod
    def validate_class_block(identifier: str, methods: List[Function]=[]) -> bool:

        is_valid = True
        if len(methods) > 0:
            is_valid = (identifier in [method.identifier for method in methods])
        return is_valid

    def __str__(self):

        class_block_string = "{\n"
        for method in self.methods:
            class_block_string += f"\t{method}\n"

        class_block_string += "}\n"

        return class_block_string

    def __repr__(self):
        return f"ClassBlock({len(self.methods)})"

    # TODO: regulate tabs in fancy string representation by external visitor
