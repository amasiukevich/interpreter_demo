from typing import List

from src.utils.program3.values.value import Value
from src.utils.program3.values.iterative_getter import IterativeGetter


class ComplexGetter(Value):

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
