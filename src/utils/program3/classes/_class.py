from src.utils.program3.node import Node
from src.utils.program3.classes.class_block import ClassBlock


class Class(Node):

    def __init__(self, identifier: str, class_block: ClassBlock):

        if  ClassBlock.validate_class_block(identifier, class_block.methods):
            self.identifier = identifier
            self.class_block = class_block
        else:
            # TODO: Custom exception here
            raise Exception("Class block should contain the costructor of the same name as class")

    def __str__(self):
        return f"class {self.identifier} {self.class_block}"

    def __repr__(self):
        return f"Class(identifier=\"{self.identifier}\")"

    # TODO: regulate tabs in string representation using external visitor
