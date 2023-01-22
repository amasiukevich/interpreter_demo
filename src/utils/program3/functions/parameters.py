from typing import List

from src.exceptions import ValidationException
from src.utils import check_unique_names
from src.utils.program3.node import Node
from src.utils.visitor import Visitor


class Parameters(Node):

    def __init__(self, has_this: bool = False, param_names: List[str] = []):

        if not check_unique_names(param_names):
            raise ValidationException("Param names should be unique")

        self.is_method = has_this
        self.param_names = param_names

    def __len__(self):
        return len(self.param_names) + 1 if self.is_method else len(self.param_names)

    def get_param_names(self):
        return self.param_names

    def __str__(self):

        to_param_string = []
        if self.is_method:
            to_param_string = ["this"] + self.param_names

        param_string = ", ".join(to_param_string)

        return param_string

    def __repr__(self):
        return f"Parameters(is_method={self.is_method}, n_params={len(self.param_names)})"

    def accept(self, visitor: Visitor):
        visitor.visit_parameters(self)

    # TODO: Keep in mind that a function can have 0 parameters in visitor!!!

    # TODO: Modify string representation by external visitor
