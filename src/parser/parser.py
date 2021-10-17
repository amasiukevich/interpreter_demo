from src.exceptions.parsing_exception import ParsingException
from src.scanner.scanner import Scanner


from src.utils.program3.expressions.operators.oper_mapper import OperatorMapper
from src.utils.program3.functions.parameters import Parameters

from src.utils.program3.program import Program
from src.utils.program3.functions.function import Function
from src.utils.program3.classes._class import Class
from src.utils.program3.block import Block
from src.utils.program3.classes.class_block import ClassBlock



from src.utils.token_type import TokenType

# TODO: Add type hints to all of the methods

class Parser:

    def __init__(self, scanner: Scanner):

        self.scanner = scanner
        self.scanner.next_token()
        self.token = self.scanner.get_token()

        self.oper_mapper = OperatorMapper()

    def parse_program(self):

        functions = []
        classes = []

        while self.scanner.get_token().token_type != TokenType.EOF:

            function = self.parse_function()
            _class = self.parse_class()

            if function:
                functions.append(function)

            if _class:
                classes.append(_class)

        program = Program(functions, classes)

        return program

    def parse_function(self):

        if self.compare_and_consume(TokenType.DEFINE):

            self.check_current_token(
                token_type=TokenType.IDENTIFIER,
                error_msg=f"{self.scanner.get_token().position}: Missing identifier while creating a function"
            )
            identifier = self.scanner.get_token_and_move()
            # construct parameters

            self.must_be_token(TokenType.OPEN_PARENTHESIS)

            parameters = self.parse_parameters()

            self.must_be_token(TokenType.CLOSING_PARENTHESIS)

            # construct block
            block = self.parse_block()

            # construct function
            the_function = Function(identifier.value, parameters, block)

            return the_function

    def parse_class(self):

        if self.compare_and_consume(TokenType.CLASS):

            self.check_current_token(
                token_type=TokenType.IDENTIFIER,
                error_msg=f"{self.scanner.get_token().position}: Missing identifier while creating a class"
            )

            identifier = self.scanner.get_token_and_move()

            # construct class block
            class_block = self.parse_class_block()

            # construct class
            _class = Class(identifier.value, class_block)

            return _class

    def parse_parameters(self):

        param_names = []
        if self.compare_and_consume(TokenType.IDENTIFIER):

            identifier = self.scanner.get_token_and_move()
            param_names.append(identifier.value)

            while self.compare_and_consume(TokenType.COMMA):
                self.check_current_token(TokenType.IDENTIFIER)
                identifier = self.scanner.get_token_and_move()
                param_names.append(identifier.value)

        params = Parameters(param_names=param_names)
        return params

    def parse_block(self):

        if self.compare_and_consume(TokenType.OPEN_CURLY_BRACKET):

            statements = []
            # parse statements
            statement = self.parse_statement()

            while statement:
                statements.append(statement)
                statement = self.parse_statement()

            self.must_be_token(
                TokenType.CLOSING_CURLY_BRACKET,
                f"{self.scanner.get_token().position}: Missing closing bracket."
            )

            block = Block(statements=statements)

            return block

    def parse_class_block(self):

        methods = []
        if self.compare_and_consume(TokenType.OPEN_CURLY_BRACKET):

            method = self.parse_function()

            while method:
                methods.append(method)
                method = self.parse_function()

            self.must_be_token(
                TokenType.CLOSING_CURLY_BRACKET,
                f"{self.scanner.get_token().position}: Missing closing bracket."
            )
            class_block = ClassBlock(methods=methods)

            return class_block

    def parse_statement(self):
        pass

    def parse_conditional(self):
        pass

    def parse_loop(self):
        pass

    def parse_while_loop(self):
        pass

    def parse_foreach_loop(self):
        pass

    def parse_assign(self):
        pass

    def parse_return(self):
        pass

    def parse_reflect(self):
        pass

    def parse_comment(self):
        pass

    def parse_function_call(self):
        pass

    def parse_value_getter(self):
        pass

    def parse_basic_value_getter(self):
        pass

    def parse_or_expression(self):
        pass

    def parse_and_expression(self):
        pass

    def parse_eq_expression(self):
        pass

    def parse_rel_expression(self):
        pass

    def parse_add_expression(self):
        pass

    def parse_mult_expression(self):
        pass

    def parse_unary_expression(self):
        pass

    # TODO: add more expressions there

    def check_current_token(self, token_type: TokenType, error_msg: str=""):
        token = self.scanner.get_token()
        if not self.compare_token_types(token_type):
            raise ParsingException(token=token,
                                   ext_token_type=token_type,
                                   message=error_msg)

    def compare_token_types(self, token_type: TokenType) -> bool:
        return self.scanner.get_token().token_type == token_type

    def compare_and_consume(self, token_type: TokenType) -> bool:

        result = self.compare_token_types(token_type)
        if result:
            self.scanner.next_token()

        return result

    # TODO: info in the exception: Missing 'something' to build 'something'
    def must_be_token(self, token_type: TokenType, error_msg: str=""):
        self.check_current_token(token_type, error_msg=error_msg)
        self.scanner.next_token()

