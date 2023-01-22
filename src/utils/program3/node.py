from abc import ABCMeta, abstractmethod

from src.utils.visitor import Visitor


class Node(metaclass=ABCMeta):

    @abstractmethod
    def accept(self, visitor: Visitor):
        pass
