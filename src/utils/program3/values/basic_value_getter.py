from src.utils.program3.node import Node
from src.utils.program3.statements.rest_function_call import RestFunctionCall
from src.utils.program3.expressions.math.add_expression import AddExpression


class BasicValueGetter(Node):

    def __init__(self, identifier: str, rest_function_call: RestFunctionCall, slicing_expr: AddExpression):

        self.identifier = identifier
        self.rest_function_call = rest_function_call
        self.slicing_expr = slicing_expr

    def get_identifier(self):
        return self.identifier

    def get_rest_func_call(self):
        return self.rest_function_call

    def get_slicing_expr(self):
        return self.slicing_expr


    def __str__(self):

        basic_value_getter_string = f"{self.identifier}"
        if bool(self.rest_function_call):
            basic_value_getter_string += f"{self.rest_function_call}"

        if bool(self.slicing_expr):
            basic_value_getter_string += f"[{self.slicing_expr}]"

        return basic_value_getter_string

    def __repr__(self):
        return f"BasicValueGetter(identifier=\"{self.identifier}\", " \
               f"has_call={self.rest_function_call is not None}" \
               f"has_slicing={self.slicing_expr is not None})"
