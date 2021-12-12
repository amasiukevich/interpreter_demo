from abc import ABCMeta

from src.utils.program3.values.value import Value


class Literal(Value, metaclass=ABCMeta):

    BOOLEAN_FILTER = {
        "true": True,
        "false": False
    }
