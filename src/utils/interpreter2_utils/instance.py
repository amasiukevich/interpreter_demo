from typing import List

from src.utils.program3.classes._class import Class
from src.exceptions import RuntimeException
from src.utils.program3.values.value import Value
from src.utils.program3.functions.function import Function
from src.utils.interpreter2_utils.scope import Scope
from src.utils.program3.variable import Variable


class Instance(Value):

    def __init__(self, klass: Class):
        self.klass = klass
        self.constructor_params = []
        self.scope = Scope()

        # for tostring
        self.value = f"Instance of type {self.klass.identifier} at {hex(id(self))}"

    def init_scope(self):

        for method in self.klass.class_block.methods:
            self.scope.add_variable(Variable(name=method.identifier, value=method))

