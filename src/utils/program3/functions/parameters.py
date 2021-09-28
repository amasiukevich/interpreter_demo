from typing import List, Optional

from src.utils.program3.node import Node
from src.utils.helpers import check_unique_names

class Parameters(Node):

    def __init__(self, has_this: bool, param_names: List[Optional, str]):

        # TODO: Custom exception here
        if not check_unique_names(param_names):
            raise Exception("Param names should be unique")

        self.param_names = param_names

    # TODO: Add fancy representation of the class
    def __str__(self):
        pass

    # TODO: Make it useful for testing
    def __repr__(self):
        pass