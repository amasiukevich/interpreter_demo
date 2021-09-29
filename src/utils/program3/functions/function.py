from src.utils.program3.node import Node
from src.utils.program3.functions.parameters import Parameters
from src.utils.program3.block import Block


class Function(Node):

    def __init__(self, identifier: str, params: Parameters, block: Block):
        self.identifier = identifier
        self.params = params
        self.block = block

    def __str__(self):
        return f"define {self.identifier}({self.params}) {self.block}"

    def __repr__(self):
        return f"Function(identifier=\"{self.identifier}\", n_params={len(self.params)}, block={self.block.__repr__()}"


    # TODO: modify the tabs using external visitor