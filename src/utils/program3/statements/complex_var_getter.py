from src.utils.program3.statements.statement import Statement
from src.utils.program3.values.this_value_getter import ThisValueGetter
from src.utils.program3.values.value_getter import RestValueGetter
from src.utils.program3.values.no_call_value_getter import NoCallValueGetter

from typing import Union

OptionalTVG = Union[ThisValueGetter, None]
OptionalRVG = Union[RestValueGetter, None]


class ComplexVarGetter(Statement):

    def __init__(self, this_value_getter: OptionalTVG, rest_value_getter: OptionalRVG, no_call_value_getter: NoCallValueGetter):

        self.this_value_getter = this_value_getter
        self.rest_value_getter = rest_value_getter
        self.no_call_value_getter = no_call_value_getter

    def __str__(self):

        complex_var_getter_string = ""
        if self.this_value_getter:
            complex_var_getter_string += f"{self.this_value_getter}"

        if self.rest_value_getter:
            complex_var_getter_string += f"{self.rest_value_getter}."

        complex_var_getter_string += f"{self.no_call_value_getter}"

        return complex_var_getter_string

    def __repr__(self):
        return f"ComplexVarGetter(has_this={bool(self.this_value_getter)}, " \
               f"has_rest_getter={bool(self.rest_value_getter)})"
