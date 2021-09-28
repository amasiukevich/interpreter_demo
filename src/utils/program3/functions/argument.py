from src.utils.program3.node import Node


class Argument(Node):

    def __init__(self, is_by_ref: bool):

        self.is_by_ref = is_by_ref
        pass

    # TODO: Add fancy representation there
    def __str__(self):
        pass

    # TODO: Make it useful for testing
    def __repr__(self):
        pass

    # TODO: Implement visiting logic with "by_ref"
