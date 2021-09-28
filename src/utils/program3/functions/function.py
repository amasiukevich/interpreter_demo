from src.utils.program3.node import Node
from src.utils.program3.functions.parameters import Parameters
from src.utils.program3.block import Block

class Function(Node):

    def __init__(self, identifier: str, params: Parameters, block: Block):
        self.identifier = identifier
        self.params = params
        self.block = block

    # TODO: Add fancy representation of the class
    def __str__(self):
        pass

    # TODO: Make it useful for testing
    def __repr__(self):
        pass