from abc import ABCMeta

from src.utils.program3.node import Node
from src.utils.visitor_old import Visitor


class Statement(Node):

    def accept(self, visitor: Visitor):
        visitor.visit_statement(self)
