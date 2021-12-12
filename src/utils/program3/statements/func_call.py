from src.exceptions import ValidationException
from src.utils.program3.statements.statement import Statement
from src.utils.program3.values.complex_getter import ComplexGetter


class FunctionCall(Statement):

    def __init__(self, complex_getter: ComplexGetter):

        if FunctionCall.validate_function_call(complex_getter):
            self.complex_getter = complex_getter

    @staticmethod
    def validate_function_call(complex_getter: ComplexGetter):
        if complex_getter.iterative_getters[-1].slicing_expr is not None or \
            complex_getter.iterative_getters[-1].rest_func_call is None:

            raise ValidationException("Invalid function call")
        return True

    def __str__(self):
        return f"{self.complex_getter};"

    def __repr__(self):
        return "FunctionCall()"
