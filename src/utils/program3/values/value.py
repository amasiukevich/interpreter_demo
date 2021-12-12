from abc import ABCMeta

from src.utils.program3.expressions.expression import Expression


class Value(Expression, metaclass=ABCMeta):
    pass
