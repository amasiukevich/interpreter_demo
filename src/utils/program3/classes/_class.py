from src.exceptions import ValidationException
from src.utils.program3.node import Node
from src.utils.program3.classes.class_block import ClassBlock
from src.utils.visitor import Visitor


class Class(Node):

    def __init__(self, identifier: str, class_block: ClassBlock):

        if ClassBlock.validate_class_block(identifier, class_block.methods):
            self.identifier = identifier
            self.class_block = class_block
        else:
            raise ValidationException("Class block should contain the costructor of the same name as class")

    def get_constructor(self):
        constructor_arr = [method for method in self.get_methods() if method.identifier == self.identifier]
        if len(constructor_arr) == 1:
            return constructor_arr[0]
        else:
            raise Exception("A class should contain exactly one constructor method of the same name as class")

    def get_methods(self):
        return self.class_block.methods

    def __str__(self):
        return f"class " \
               f"{self.identifier} {self.class_block}"

    def __repr__(self):
        return f"Class(identifier=\"{self.identifier}\")"

    def accept(self, visitor: Visitor):
        visitor.visit_class(self)

    # TODO: regulate tabs in string representation using external visitor
