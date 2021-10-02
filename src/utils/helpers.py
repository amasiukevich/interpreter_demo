# from src.utils.program3.expressions.expression import Expression
# from src.utils.program3.expressions.operators.operator import Operator
# from src.utils.program3.values.basic_value_getter import BasicValueGetter

from typing import List


def check_unique_names(list_of_names: List[str]) -> bool:
    return len(set(list_of_names)) == len(list_of_names)


# def validate_expressions_types(base_class_name: str, expressions: List[Expression] = []) -> bool:
#
#     if len(expressions) > 0 and not all([isinstance(expr, Expression) for expr in expressions]):
#         # TODO: custom exception here
#         raise Exception(f"All {base_class_name} components should be of Expression datatype")
#     return True
#
#
# def validate_operator_types(base_class_name: str, operators: List[Operator]) -> bool:
#
#     if len(operators) > 0 and not all([isinstance(oper, Operator) for oper in operators]):
#         # TODO: Custom exception here
#         raise Exception(f"All {base_class_name} components should be of Operator datatype")
#     return True


# def validate_differs_in_one(expressions: List[Expression], operators: List[Operator]) -> bool:
#
#     if len(expressions) - len(operators) != 1:
#         # TODO: Custom exception here
#         raise Exception(f"Number of exception components should be greater than number of operators by exactly 1")
#     return True

# TODO: Move it to the base class
# def validate_basic_getters(base_class_name: str, basic_getters: List[BasicValueGetter]) -> bool:
#
#     if len(basic_getters) < 1:
#         # TODO: custom exception here
#         raise Exception(f"Cannot construct {base_class_name} without basic value getters")
#
#     elif not all([isinstance(base_getter, BasicValueGetter) for base_getter in basic_getters]):
#         # TODO: custom exception here
#         raise Exception(f"All {base_class_name} components should be of BasicValueGetter datatype")
#
#     return True
