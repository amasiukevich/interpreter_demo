from src.utils.program3.expressions.expression import Expression
from src.utils.program3.values.complex_getter import ComplexGetter
from src.utils.program3.statements.statement import Statement


class Assign(Statement):

    def __init__(self, complex_getter: ComplexGetter, expression: Expression):

        self.complex_getter = complex_getter
        self.expression = expression

    def __str__(self):
        return f"{self.complex_getter} = {self.expression}"

    def __repr__(self):
        return f"Assign(complex_var_getter={self.complex_getter.__repr__()}, " \
               f"expression={self.expression.__repr__()})"

    # TODO: Fancy tostring using visitor
