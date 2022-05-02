from src.utils.program3.statements.statement import Statement
from src.utils.program3.statements.complex_getter import ComplexGetter
from src.utils.visitor import Visitor


class FunctionCall(Statement):

    def __init__(self, complex_getter: ComplexGetter):

        self.getter = complex_getter
        self.callee_name = self.getter.get_last_identifier()
        self.arguments = self.getter.get_call_arguments()

    def get_arguments(self):
        return self.arguments.arguments

    def get_callee_name(self):
        return self.callee_name

    def __str__(self):
        return f"{self.getter};"

    def __repr__(self):
        return "FunctionCall();"

    def accept(self, visitor: Visitor):
        visitor.visit_function_call(self)
