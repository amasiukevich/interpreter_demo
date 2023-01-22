from src.utils.program3.expressions.math.add_expression import AddExpression
from src.utils.program3.functions.arguments import Arguments
from src.utils.program3.statements.rest_function_call import RestFunctionCall
from src.utils.program3.values.value import Value
from src.utils.visitor import Visitor


# class IterativeGetter(Value):
#
#     def __init__(self, identifier: str,
#                  rest_func_call: RestFunctionCall=None,
#                  slicing_expr: AddExpression=None):
#
#         # TODO: Make internal object of identifier / function call / slicing
#         # TODO: adapt visitor
#         self.identifier = identifier
#         self.rest_func_call = rest_func_call
#         self.slicing_expr = slicing_expr
#
#     def get_identifier(self) -> str:
#         return self.identifier
#
#     def get_rest_funct_call(self) -> RestFunctionCall:
#         return self.rest_func_call
#
#     def get_slicing_expr(self) -> AddExpression:
#         return self.slicing_expr
#
#     def __str__(self):
#
#         ig_components = [self.identifier]
#         if bool(self.rest_func_call):
#             ig_components.append(str(self.rest_func_call))
#
#         if bool(self.slicing_expr):
#             ig_components.append("[" + str(self.slicing_expr) + "]")
#
#         return "".join(ig_components)
#
#     def __repr__(self):
#         return f"IterativeGetter(identifier=\"{self.identifier}\", " \
#                f"has_call={self.rest_func_call is not None}, " \
#                f"has_slicing={self.slicing_expr is not None})"
#
#     def accept(self, visitor: Visitor):
#         visitor.visit_iterative_getter(self)


class IterativeGetter(Value):
    
    def __init__(self, identifier: str, arguments: Arguments=None):
        self.arguments = arguments
        self.identifier = identifier


class IdentifierGetter(IterativeGetter):

    def __init__(self, identifier):
        super().__init__(identifier)
        self.identifier = identifier

    def __str__(self):
        return self.identifier

    def __repr__(self):
        return f"IdentifierGetter(identifier={self.identifier})"

    def get_identifier(self):
        return self.identifier

    def accept(self, visitor: Visitor):
        return visitor.visit_identifier_getter(self)


class CallGetter(IterativeGetter):

    def __init__(self, identifier: str, arguments: Arguments):
        super().__init__(identifier, arguments)
        self.identifier = identifier
        self.arguments = arguments

    def __str__(self):
        return f"{self.identifier}({self.arguments})"

    def __repr__(self):
        return f"IdentifierGetter(identifier={self.identifier})"

    def get_identifier(self):
        return self.identifier

    def get_arguments(self):
        return self.arguments.arguments

    def accept(self, visitor: Visitor, scope_to_push=None):
        visitor.visit_call_getter(self, scope_to_push)


# TODO: Maybe slicing after call getter