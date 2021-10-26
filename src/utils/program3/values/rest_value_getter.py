from src.utils.program3.node import Node
from src.utils.program3.values.basic_value_getter import BasicValueGetter
# from src.utils.helpers import validate_basic_getters

from typing import List


class RestValueGetter(Node):

    def __init__(self, base_getters: List[BasicValueGetter]):

        # TODO: create validation
        # if validate_basic_getters(self.__class__.__name__, base_getters):

        self.basic_getters = base_getters

    def get_basic_getters(self):
        return self.basic_getters

    def __str__(self):
        return ".".join([f"{basic_getter}" for basic_getter in self.basic_getters])

    def __repr__(self):
        return f"RestValueGetter({len(self.basic_getters)})"
