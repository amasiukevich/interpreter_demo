from src.utils.program3.values.value import Value
from src.utils.program3.values.this_value_getter import ThisValueGetter
from src.utils.program3.values.rest_value_getter import RestValueGetter
from src.utils.program3.values.no_call_value_getter import NoCallValueGetter
from src.utils.program3.values.basic_value_getter import BasicValueGetter

from typing import Union

OptionalTVG = Union[ThisValueGetter, None]
OptionalRVG = Union[RestValueGetter, None]
GeneralLastGetter = Union[NoCallValueGetter, BasicValueGetter]


class ComplexValueGetter(Value):

    def __init__(self,
                 this_value_getter: OptionalTVG,
                 rest_value_getter: OptionalRVG,
                 last_getter: GeneralLastGetter):

        self.this_value_getter = this_value_getter
        self.rest_value_getter = rest_value_getter


        self.last_value_getter = last_getter

    def __str__(self):

        complex_var_getter_string = ""
        if self.this_value_getter:
            complex_var_getter_string += f"{self.this_value_getter}"

        if self.rest_value_getter:
            complex_var_getter_string += f"{self.rest_value_getter}."

        complex_var_getter_string += f"{self.last_value_getter}"

        return complex_var_getter_string

    def __repr__(self):
        return f"ComplexVarGetter(has_this={bool(self.this_value_getter)}, " \
               f"has_rest_getter={bool(self.rest_value_getter)})"
