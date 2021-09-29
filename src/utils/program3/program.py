from typing import List, Union
from src.utils.helpers import check_unique_names

from src.utils.program3.node import Node
from src.utils.program3.functions.function import Function
from src.utils.program3.classes._class import Class

class Program(Node):

    # TODO: At least one function
    def __init__(self, functions: List[Function], classes: List[Class] = []):

        if Program.validate_functions(functions):
            self.functions = functions
            self.function_dict = {function.identifier: function for function in functions}

        if Program.validate_classes(classes):
            self.classes = classes
            self.class_dict = {_class.identifier: _class for _class in classes}

    @staticmethod
    def validate_functions(functions: List[Function]) -> bool:
        return Program.validate_main_presence(functions) and Program.validate_unique_functions(functions)

    @staticmethod
    def validate_classes(classes: List[Class]) -> bool:
        return Program.validate_unique_classes(classes)

    @staticmethod
    def validate_main_presence(functions: List[Function]) -> bool:
        is_valid = True
        if not (len(functions) > 0 and "main" in [function.identifier for function in functions]):
            # TODO: Custom exception here
            raise Exception("Program should contain at least one function, which is main function")
        return is_valid

    @staticmethod
    def validate_unique_functions(functions: List[Function]) -> bool:
        is_valid = True
        if not check_unique_names([function.identifier for function in functions]):
            # TODO: Custom exception here
            raise Exception("Function names must be unique")
        return is_valid

    @staticmethod
    def validate_unique_classes(classes: List[Class]) -> bool:
        is_valid = True
        if not check_unique_names([_class.identifier for _class in classes]):
            # TODO: custom exception here
            raise Exception("Class names must be unique")
        return is_valid

    def add_function(self, function: Function):

        if not check_unique_names(list(self.function_dict.keys()) + [function.identifier]):
            # TODO: Custom exception here
            raise Exception(f"Function of name {function.identifier} already exists")

        self.functions.append(function)
        self.function_dict.update({function.identifier: function})

    def add_class(self, _class: Class):

        if not check_unique_names(list(self.class_dict.keys()) + [_class.identifier]):
            # TODO: Custom exception here
            raise Exception(f"Class of name {_class.identifier} already exists")

        self.classes.append(_class)
        self.class_dict.update({_class.identifier: _class})

    def get_function(self, identifier: str) -> Union[Function, None]:
        return self.function_dict.get(identifier)

    def get_class(self, identifier: str) -> Union[Class, None]:
        return self.class_dict.get(identifier)

    def __str__(self):

        program_string = ""
        for function in self.functions:
            program_string += f"{function}\n\n"

        for cls in self.classes:
            program_string += f"{cls}\n\n"

        return program_string

    def __repr__(self):
        return f"Program(n_functions={len(self.functions)}, n_classes={len(self.classes)})"
