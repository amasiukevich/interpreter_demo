from src.utils.program3.node import Node
from src.utils.program3.functions.arguments import Arguments
from src.utils.visitor import Visitor


class RestFunctionCall(Node):

    def __init__(self, arguments: Arguments):
        self.arguments = arguments

    def __str__(self):
        return f"({self.arguments})"

    def __repr__(self):
        return "RestFunctionCall()"

    def accept(self, visitor: Visitor):
        visitor.visit_rest_function_call(self)
