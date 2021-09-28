from typing import List, Optional

from src.utils.program3.node import Node
from src.utils.program3.functions.function import Function


class ClassBlock(Node):

    def __init__(self, methods: List[Function, Optional]):
        self.methods = methods

    # TODO: Make a fancy representation of the class
    def __str__(self):
        pass

    # TODO: Make it useful for testing
    def __repr__(self):
        pass