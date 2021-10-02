from src.utils.program3.values.value import Value
from src.utils.program3.values.this_value_getter import ThisValueGetter
from src.utils.program3.values.rest_value_getter import RestValueGetter


class ValueGetter(Value):

    def __init__(self, this_value_getter: ThisValueGetter = None, rest_value_getter: RestValueGetter = None):

        self.this_value_getter = this_value_getter
        self.rest_value_getter = rest_value_getter

    def __str__(self):

        value_getter_string = ""
        if self.this_value_getter:
            value_getter_string += f"{self.this_value_getter}"

        value_getter_string += f"{self.rest_value_getter}"

        return self.rest_value_getter

    def __repr__(self):
        return f"ValueGetter(has_this={bool(self.this_value_getter)})"
