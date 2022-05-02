from typing import List

from src.utils.program3.statements.statement import Statement
from src.utils.program3.values.value import Value

from src.utils.program3.values.iterative_getter import IterativeGetter
from src.utils.visitor import Visitor


class ComplexGetter(Statement, Value):

    def __init__(self, has_this: bool, iterative_getters: List[IterativeGetter]):
        self.has_this = has_this
        self.iterative_getters = iterative_getters

    def __str__(self):
        cvg_components = []
        if self.has_this:
            cvg_components.append("this")
        for getter in self.iterative_getters:
            cvg_components.append(str(getter))
        return ".".join(cvg_components)

    def __repr__(self):
        return f"ComplexGetter(has_this={self.has_this}, " \
               f"num_iterative_getters={len(self.iterative_getters)})"

    def get_last_getter(self):
        return self.iterative_getters[-1]

    def get_last_identifier(self):
        try:
            return self.iterative_getters[-1].identifier
        except:
            print("Hey ther")

    def get_call_arguments(self):
        return self.iterative_getters[-1].arguments

    def accept(self, visitor: Visitor, is_assign=(False, None)):
        return visitor.visit_complex_getter(self, is_assign=is_assign)
