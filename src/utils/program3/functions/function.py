from src.utils.program3.node import Node
from src.utils.interpreter_utils.call_utils import AbcFunction
from src.utils.program3.block import Block
from src.utils.program3.functions.parameters import Parameters
from src.utils.visitor import Visitor


class Function(Node, AbcFunction):

    def __init__(self, identifier: str, params: Parameters, block: Block):
        self.identifier = identifier
        self.params = params
        self.block = block

    def __str__(self):
        return f"{self.identifier}({self.params}) {self.block}"

    def __repr__(self):
        return f"Function(identifier=\"{self.identifier}\", n_params={len(self.params)}, block={self.block.__repr__()}"

    def get_params(self):
        return self.params

    def get_param_names(self):
        return self.params.get_param_names()

    def get_block(self):
        return self.block

    def accept(self, visitor: Visitor):
        visitor.visit_function(self)

    # TODO: modify the tabs using external visitor
