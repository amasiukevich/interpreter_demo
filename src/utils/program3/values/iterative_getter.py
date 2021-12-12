from src.utils.program3.expressions.math.add_expression import AddExpression
from src.utils.program3.statements.rest_function_call import RestFunctionCall
from src.utils.program3.values.value import Value


class IterativeGetter(Value):

    def __init__(self, identifier: str,
                 rest_func_call: RestFunctionCall=None,
                 slicing_expr: AddExpression=None):

        self.identifier = identifier
        self.rest_func_call = rest_func_call
        self.slicing_expr = slicing_expr

    def get_identifier(self) -> str:
        return self.identifier

    def get_rest_funct_call(self) -> RestFunctionCall:
        return self.rest_func_call

    def get_slicing_expr(self) -> AddExpression:
        return self.slicing_expr

    def __str__(self):

        ig_components = [self.identifier]
        if bool(self.rest_func_call):
            ig_components.append(str(self.rest_func_call))

        if bool(self.slicing_expr):
            ig_components.append("[" + str(self.slicing_expr) + "]")

        return "".join(ig_components)

    def __repr__(self):
        return f"IterativeGetter(identifier=\"{self.identifier}\", " \
               f"has_call={self.rest_func_call is not None}, " \
               f"has_slicing={self.slicing_expr is not None})"
