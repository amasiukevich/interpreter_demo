from typing import List

from src.utils.program3.classes._class import Class
from src.exceptions import RuntimeException
from src.utils.program3.values.value import Value
from src.utils.program3.functions.function import Function
from src.utils.interpreter2_utils.environment import Environment


class Instance(Value):

    def __init__(self, klass: Class):
        self.klass = klass
        self.environment = Environment()

        # for tostring
        self.value = f"Instance of type {self.klass.identifier} at {hex(id(self))}"
