from typing import List, Optional

from src.utils.program3.node import Node
from src.utils.program3.functions.argument import Argument

class Arguments(Node):

    def __init__(self, arguments: List[Argument, Optional]):
        self.arguments = arguments

    # TODO: Add fancy representation there
    def __str__(self):
        pass

    # TODO: Make it useful for testing
    def __repr__(self):
        pass