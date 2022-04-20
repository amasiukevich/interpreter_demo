from abc import ABCMeta

from src.utils.program3.values.value import Value
from src.utils.visitor_old import Visitor


class Literal(Value, metaclass=ABCMeta):

    BOOLEAN_FILTER = {
        "true": True,
        "false": False
    }

    def __init__(self):
        self.value = None

    def accept(self, visitor: Visitor):
        pass
