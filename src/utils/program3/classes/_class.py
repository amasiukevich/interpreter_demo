from src.utils.program3.node import Node
from src.utils.program3.classes.class_block import ClassBlock


class Class(Node):

    def __init__(self, identifier: str, class_block: ClassBlock):

        self.identifier = identifier
        self.class_block = class_block

    # TODO: Make fancy representation of the class here
    def __str__(self):
        pass

    # TODO: Make it useful for testing
    def __repr__(self):
        pass
