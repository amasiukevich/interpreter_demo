from src.utils.program3.node import Node
from src.utils.program3.statements.complex_var_getter import ComplexVarGetter
from src.utils.program3.expressions.expression import Expression


class Assign(Node):

    def __init__(self, complex_var_getter: ComplexVarGetter, expression: Expression):

        self.complex_var_getter = complex_var_getter
        self.expression = expression

    def __str__(self):
        return f"{self.complex_var_getter} = {self.expression}"

    def __repr__(self):
        return f"Assign(complex_var_getter={self.complex_var_getter.__repr__()}, " \
               f"expression={self.expression.__repr__()})"
