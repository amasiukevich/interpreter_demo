from abc import ABCMeta

from src.utils.program3.functions.function import Function
from .environment import DummyEnvironment
from ...exceptions import RuntimeException


class PeramolangCallable(metaclass=ABCMeta):

    def call(self, interpreter, arguments):
        """
        :param interpreter: just in case the implementing class needs it
        :param arguments: lsit of evaluated argument expressions
        :return:
        """
        pass

    def get_arity(self) -> int:
        """
        :return: number of parameters in the callable function
        """
        pass


class NativeFunction(PeramolangCallable):

    def __init__(self, call_func, arity):
        self.call_func = call_func
        self.arity = arity

    def call(self, interpreter, arguments):
        self.call_func(interpreter, arguments)

    def get_arity(self) -> int:
        return self.arity


class PeramolangFunction(PeramolangCallable):

    def __init__(self, function: Function):
        self.environment = None
        self.function_decl = function

    def call(self, interpreter, arguments):

        self.environment = DummyEnvironment(interpreter.environment)
        parameters = self.function_decl.get_params().param_names
        if arguments and parameters:
            for param, arg in zip(
                    self.function_decl.get_params().param_names,
                    arguments):
                self.environment.define(param, arg)
        try:
            interpreter.execute_block(self.function_decl.block, self.environment)
        except ReturnObj as return_val:
            return return_val.value

    def get_arity(self):
        return len(self.function_decl.get_params())

    def __repr__(self):
        return f"<fn {self.function_decl.identifier}>"


# TODO: Implement return without throwing an exception
class ReturnObj(RuntimeException):

    def __init__(self, return_statement):
        super().__init__(token=None, message=None)
        self.value = return_statement.expression
