from typing import Optional, Union

from src.exceptions import ParsingException, ValidationException
from src.scanner.scanner import Scanner

# Common utils
from src.utils.program3.statements.func_call import FunctionCall
from src.utils.program3.values.literals.null_literal import NullLiteral
from src.utils.token import Token
from src.utils.token_type import TokenType

# General
from src.utils.program3.program import Program
from src.utils.program3.block import Block

# Classes
from src.utils.program3.classes._class import Class
from src.utils.program3.classes.class_block import ClassBlock

# Functions
from src.utils.program3.functions.function import Function
from src.utils.program3.functions.parameters import Parameters
from src.utils.program3.functions.arguments import Arguments

# Statements
from src.utils.program3.statements.statement import Statement
from src.utils.program3.statements.assign import Assign
from src.utils.program3.statements.comment import Comment
from src.utils.program3.statements.conditional import Conditional
from src.utils.program3.statements.foreach_loop import ForeachLoop
from src.utils.program3.statements.rest_function_call import RestFunctionCall
from src.utils.program3.statements.while_loop import WhileLoop
from src.utils.program3.statements._return import Return
from src.utils.program3.values.complex_getter import ComplexGetter
from src.utils.program3.values.iterative_getter import IterativeGetter, IdentifierGetter, CallGetter

# Expressions
from src.utils.program3.expressions.expression import Expression
from src.utils.program3.expressions.math.add_expression import AddExpression
from src.utils.program3.expressions.math.and_expression import AndExpression
from src.utils.program3.expressions.math.equality_expression import EqualityExpression
from src.utils.program3.expressions.math.multiply_expression import MultiplyExpression
from src.utils.program3.expressions.math.or_expression import OrExpression
from src.utils.program3.expressions.math.relation_expression import RelationExpression
from src.utils.program3.expressions.math.unary_expression import UnaryExpression

# Operators
from src.utils.program3.expressions.operators.operator import Operator
from src.utils.program3.expressions.operators.oper_mapper import OperatorMapper

# Values
from src.utils.program3.values.value import Value
from src.utils.program3.values.literals.literal import Literal
from src.utils.program3.values.literals.bool_literal import BoolLiteral
from src.utils.program3.values.literals.float_literal import FloatLiteral
from src.utils.program3.values.literals.int_literal import IntLiteral
from src.utils.program3.values.literals.string_literal import StringLiteral


class Parser:

    def __init__(self, scanner: Scanner):

        self.scanner = scanner
        self.scanner.next_token()
        self.token = self.scanner.get_token()

        self.oper_mapper: OperatorMapper= OperatorMapper()

    def parse_program(self) -> Optional[Program]:

        functions = []
        classes = []

        while (function := self.parse_function()) or (_class := self.parse_class()):

            if function:
                functions.append(function)
                function = None

            if _class:
                classes.append(_class)
                _class = None

        # try:
        self.must_be_token(TokenType.EOF)
        # except Exception:
        #     print("Hey there")
        program = Program(functions, classes)

        return program

    def parse_function(self) -> Optional[Function]:

        if self.compare_token_types(TokenType.IDENTIFIER):

            identifier = self.scanner.get_token_and_move()

            # Constructing parameters
            self.must_be_token(TokenType.OPEN_PARENTHESIS)
            parameters = self.parse_parameters()
            self.must_be_token(
                TokenType.CLOSING_PARENTHESIS,
                error_msg=f"{self.scanner.get_token().position}: Missing closing parenthesis"
            )

            block = self.parse_block()

            the_function = Function(identifier.value, parameters, block)

            return the_function

    def parse_class(self) -> Optional[Class]:

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

    def parse_parameters(self) -> Optional[Parameters]:

        has_this = False
        param_names = []
        if self.compare_and_consume(TokenType.THIS):
            has_this = True
        elif self.compare_token_types(TokenType.IDENTIFIER):
            identifier = self.scanner.get_token_and_move()
            param_names.append(identifier.value)

        while self.compare_and_consume(TokenType.COMMA):
            self.check_current_token(TokenType.IDENTIFIER)
            identifier = self.scanner.get_token_and_move()
            param_names.append(identifier.value)

        params = Parameters(has_this=has_this, param_names=param_names)
        return params

    def parse_block(self) -> Optional[Block]:

        statements = []
        if self.compare_and_consume(TokenType.OPEN_CURLY_BRACKET):

            # parse statements

            while statement := self.parse_statement():
                statements.append(statement)

            self.must_be_token(
                TokenType.CLOSING_CURLY_BRACKET,
                f"{self.scanner.get_token().position}: Missing closing bracket."
            )

        return Block(statements=statements)

    def parse_class_block(self) -> Optional[ClassBlock]:

        methods = []
        if self.compare_and_consume(TokenType.OPEN_CURLY_BRACKET):

            while method := self.parse_function():
                methods.append(method)

            self.must_be_token(
                TokenType.CLOSING_CURLY_BRACKET,
                f"{self.scanner.get_token().position}: Missing closing curly bracket."
            )
            class_block = ClassBlock(methods=methods)

            return class_block

    def parse_statement(self) -> Optional[Statement]:

        # try parsing conditional
        if statement := self.parse_conditional():
            return statement

        # try parsing loops
        if statement := self.parse_while_loop():
            return statement

        if statement := self.parse_foreach_loop():
            return statement

        # try parsing return
        if statement := self.parse_return():
            return statement

        # try parsing assign or function call
        if statement := self.parse_assign_or_function_call():
            return statement

        # try parsing comment
        if statement := self.parse_comment():
            return statement

    def parse_conditional(self) -> Optional[Conditional]:

        # TODO: Check blocks on nullness
        if self.compare_and_consume(TokenType.IF):

            conditions = []
            blocks = []
            single_else_case = False

            expression = self.parse_or_expression()

            if_block = self.parse_block()
            conditions.append(expression)
            blocks.append(if_block)

            # multiple elseif blocks
            # TODO: check if the parsed components is not None
            while self.compare_and_consume(TokenType.ELSE) and not single_else_case:

                # Else if block
                if self.compare_and_consume(TokenType.IF):
                    expression = self.parse_or_expression()
                    else_if_block = self.parse_block()
                    conditions.append(expression)
                    blocks.append(else_if_block)

                # single else case
                else:
                    else_block = self.parse_block()
                    blocks.append(else_block)
                    single_else_case = True

            return Conditional(expressions=conditions, blocks=blocks)

    def parse_while_loop(self) -> Optional[WhileLoop]:

        if self.compare_and_consume(TokenType.WHILE):

            if not (condition := self.parse_or_expression()):
                raise ValidationException(
                    f"{self.scanner.get_token().position}: Condition in while loop cannot be empty")

            if not (block := self.parse_block()):
                raise ValidationException(
                    f"{self.scanner.get_token().position()}: Block in while loop cannot be empty")

            while_loop = WhileLoop(condition, block)

            return while_loop

    def parse_foreach_loop(self) -> Optional[ForeachLoop]:

        # TODO: check identifier, expression and block on nullness
        if self.compare_and_consume(TokenType.FOREACH):
            # Identifier
            self.check_current_token(TokenType.IDENTIFIER)
            identifier = self.scanner.get_token_and_move()

            # IN
            self.must_be_token(TokenType.IN)

            # or_expression
            or_expression = self.parse_or_expression()

            # block
            block = self.parse_block()

            return ForeachLoop(identifier=identifier, expression=or_expression, block=block)

    def parse_return(self) -> Optional[Return]:

        # TODO: Check returning expression
        if self.compare_and_consume(TokenType.RETURN):

            returning_expression = self.parse_or_expression()
            self.must_be_token(TokenType.SEMICOLON)

            return Return(returning_expression)

    def parse_comment(self):

        if self.compare_token_types(TokenType.COMMENT):
            token = self.scanner.get_token_and_move()
            return Comment(comment_body=token.value)

    def parse_assign_or_function_call(self) -> Optional[Union[Assign, FunctionCall]]:

        complex_getter = self.parse_complex_getter()

        if self.compare_and_consume(TokenType.ASSIGN):
            # Assign statement
            expression = self.parse_or_expression()
            self.must_be_token(TokenType.SEMICOLON)

            assign_statement = Assign(complex_getter, expression)
            return assign_statement

        elif self.compare_and_consume(TokenType.SEMICOLON):
            # TODO: Try to get it less artificial
            # meaning function call
            return FunctionCall(complex_getter)

    def parse_complex_getter(self) -> Optional[ComplexGetter]:

        has_this = False
        iter_getters = []
        if self.compare_and_consume(TokenType.THIS):
            has_this = True
        elif iter_getter := self.parse_iterative_getter():
            iter_getters.append(iter_getter)
        # TODO: alternatively use 'not recognized' flags
        else:
            return

        while self.compare_and_consume(TokenType.ACCESS):
            iter_getter = self.parse_iterative_getter()
            if iter_getter:
                iter_getters.append(iter_getter)
            else:
                raise Exception("Wrong complex_getter")

        if len(iter_getters) == 0:
            raise ValidationException(
                f"{self.scanner.get_token().position}: Complex getter should contain at least one iterative getter")

        return ComplexGetter(has_this=has_this, iterative_getters=iter_getters)


    def parse_iterative_getter(self):

        # TODO: in future maybe extend to slicings
        if self.compare_token_types(TokenType.IDENTIFIER):

            identifier = self.scanner.get_token().value
            self.scanner.next_token()

            # call getter case
            if self.compare_and_consume(TokenType.OPEN_PARENTHESIS):
                arguments = self.parse_arguments()
                self.must_be_token(TokenType.CLOSING_PARENTHESIS,
                                   f"Expected: {TokenType.CLOSING_PARENTHESIS}, got: {self.scanner.get_token().token_type}")
                return CallGetter(identifier=identifier, arguments=arguments)
            else:
                return IdentifierGetter(identifier=identifier)

    # def parse_iterative_getter(self) -> Optional[IterativeGetter]:
    #
    #     if self.compare_token_types(TokenType.IDENTIFIER):
    #
    #         identifier = self.scanner.get_token().value
    #         self.scanner.next_token()
    #
    #         rest_function_call = self.parse_rest_function_call()
    #         slicing_expr = self.parse_slicing_expr()
    #
    #         return IterativeGetter(identifier, rest_function_call, slicing_expr)

    # def parse_rest_function_call(self) -> Optional[RestFunctionCall]:
    #
    #     if self.compare_and_consume(TokenType.OPEN_PARENTHESIS):
    #
    #         arguments = self.parse_arguments()
    #         self.must_be_token(TokenType.CLOSING_PARENTHESIS,
    #                            f"Expected: {TokenType.CLOSING_PARENTHESIS}, got: {self.scanner.get_token().token_type}")
    #
    #         return RestFunctionCall(arguments)

    def parse_arguments(self) -> Optional[Arguments]:

        list_of_args = []

        if argument := self.parse_argument():
            list_of_args.append(argument)

            while self.compare_and_consume(TokenType.COMMA):
                argument = self.parse_or_expression()
                list_of_args.append(argument)

        return Arguments(arguments=list_of_args)

    def parse_argument(self):

        try:
            argument = self.parse_or_expression()
        except:
            argument = None

        return argument

    def parse_slicing_expr(self) -> Optional[AddExpression]:

        if self.compare_and_consume(TokenType.OPEN_BRACKET):
            add_expression = self.parse_add_expression()
            self.must_be_token(TokenType.CLOSING_BRACKET)

            return add_expression

    def parse_or_expression(self) -> Optional[Union[OrExpression, AndExpression]]:

        expression_components = []

        if and_expression := self.parse_and_expression():

            expression_components.append(and_expression)

            while self.compare_and_consume(TokenType.OR):
                and_expression = self.parse_and_expression()
                if not and_expression:
                    raise ValidationException(
                        f"{self.scanner.get_token().position}: Error while parsing OR Expression")

                expression_components.append(and_expression)

        if len(expression_components) == 1:
            return and_expression

        return OrExpression(expressions=expression_components)

    def parse_and_expression(self) -> Optional[Union[AndExpression, EqualityExpression]]:

        expression_components = []
        if eq_expression := self.parse_eq_expression():

            expression_components.append(eq_expression)
            while self.compare_and_consume(TokenType.AND):
                eq_expression = self.parse_eq_expression()
                if not eq_expression:
                    raise ValidationException(
                        f"{self.scanner.get_token().position}: Error while parsing AND Expression")

                expression_components.append(eq_expression)

        if len(expression_components) == 1:
            return eq_expression

        return AndExpression(expressions=expression_components)

    def parse_eq_expression(self) -> Optional[Union[EqualityExpression, RelationExpression]]:

        expression_components = []
        operator = None

        if rel_expression := self.parse_rel_expression():
            expression_components.append(rel_expression)

            if self.is_eq_token():

                operator = self.parse_operator()
                if not operator:
                    raise ValidationException(
                        f"{self.scanner.get_token().position}: Error while parsing operator in equality expression")

                rel_expression = self.parse_rel_expression()

                if not rel_expression:
                    raise ValidationException(
                        f"{self.scanner.get_token().position}: Error while parsing equality expression")
                expression_components.append(rel_expression)

        if len(expression_components) == 1:
            return rel_expression

        return EqualityExpression(
            expressions=expression_components,
            operator=operator
        )

    def is_eq_token(self) -> bool:
        token_type = self.scanner.get_token().token_type
        return token_type == TokenType.EQUAL or \
               token_type == TokenType.NOT_EQUAL

    # TODO: refactor action for parsing expressions (rel + eq)
    def parse_rel_expression(self) -> Optional[Union[RelationExpression, AddExpression]]:

        expression_components = []
        operator = None

        if add_expression := self.parse_add_expression():
            expression_components.append(add_expression)

            if self.is_rel_token():
                operator = self.parse_operator()

                if not operator:
                    raise ValidationException(
                        f"{self.scanner.get_token().position}: Error while parsing operator relation expression")

                add_expression = self.parse_rel_expression()

                if not add_expression:
                    raise ValidationException(
                        f"{self.scanner.get_token().position}: Error while parsing Relation Expression")

                expression_components.append(add_expression)

        if len(expression_components) == 1:
            return add_expression

        return RelationExpression(
            expressions=expression_components,
            operator=operator
        )

    def is_rel_token(self) -> bool:
        token_type = self.scanner.get_token().token_type
        return token_type == TokenType.GREATER or token_type == TokenType.GREATER_EQUAL or \
               token_type == TokenType.LESS or token_type == TokenType.LESS_EQUAL

    # TODO: Refactor inner loop in expressions (Add + Multiply)
    def parse_add_expression(self) -> Optional[Union[AddExpression, MultiplyExpression]]:

        expression_components = []
        operators = []

        if mult_expression := self.parse_mult_expression():

            expression_components.append(mult_expression)
            while self.is_add_token():

                operator = self.parse_operator(is_additive=True)

                if not operator:
                    raise ValidationException(
                        f"{self.scanner.get_token().position}: Error while parsing operator additive expression")
                operators.append(operator)

                mult_expression = self.parse_mult_expression()

                if not mult_expression:
                    raise ValidationException(
                        f"{self.scanner.get_token().position}: Error while parsing additive expression")
                expression_components.append(mult_expression)

        if len(expression_components) == 1:
            return mult_expression

        return AddExpression(
            expressions=expression_components,
            operators=operators
        )

    def is_add_token(self) -> bool:
        token_type = self.scanner.get_token().token_type
        return token_type == TokenType.PLUS or \
               token_type == TokenType.MINUS

    def parse_mult_expression(self) -> Optional[Union[MultiplyExpression, UnaryExpression]]:

        expression_components = []
        operators = []

        if unary_expression := self.parse_unary_expression():

            expression_components.append(unary_expression)

            while self.is_mult_token():
                operator = self.parse_operator()
                if not operator:
                    raise ValidationException(
                        f"{self.scanner.get_token().position}: Error while parsing operator in multiply expression")
                operators.append(operator)

                unary_expression = self.parse_unary_expression()

                if not unary_expression:
                    raise ValidationException(
                        f"{self.scanner.get_token().position}: Error while parsing unary expression")
                expression_components.append(unary_expression)

        if len(expression_components) == 1:
            return unary_expression

        return MultiplyExpression(
            expressions=expression_components,
            operators=operators
        )

    def is_mult_token(self) -> bool:
        token_type = self.scanner.get_token().token_type
        return token_type == TokenType.MULTIPLY or token_type == TokenType.DIVIDE or token_type == TokenType.MODULO

    def parse_unary_expression(self) -> Optional[Union[UnaryExpression, Expression]]:

        operator = None
        general_value = None
        if self.is_unary_token():
            operator = self.parse_operator()
            if not operator:
                raise ValidationException(
                    f"{self.scanner.get_token().position}: Invalid operator for unary expression")

            expression = self.parse_general_value()
            un_expr = UnaryExpression(expression=expression, operator=operator)
            return un_expr

        general_value = self.parse_general_value()

        return general_value

    def is_unary_token(self):
        token_type = self.scanner.get_token().token_type
        return token_type == TokenType.MINUS or token_type == TokenType.NOT

    def parse_general_value(self) -> Union[Value, OrExpression]:

        if self.compare_and_consume(TokenType.OPEN_PARENTHESIS):

            or_expression = self.parse_or_expression()
            self.must_be_token(TokenType.CLOSING_PARENTHESIS)

            return or_expression
        else:
            return self.parse_value()

    def parse_operator(self, is_additive=False) -> Optional[Operator]:

        token_type = self.scanner.get_token().token_type

        operator = self.oper_mapper.token_to_operator.get(token_type)
        additive_operator = self.oper_mapper.token_to_operator_additive.get(token_type)
        
        result = additive_operator if is_additive else operator

        self.scanner.next_token()
        return result

    def parse_value(self) -> Optional[Value]:

        token = self.scanner.get_token()
        value = None

        # literal case
        if self.is_literal(token.token_type):
            value = self.token_to_literal(token)
        # complex value getter
        elif self.compare_token_types(TokenType.IDENTIFIER) or self.compare_token_types(TokenType.THIS):
            value = self.parse_complex_getter()
        return value

    def token_to_literal(self, token: Token) -> Optional[Literal]:

        literal = None
        if token.token_type == TokenType.NUMERIC_LITERAL:
            if isinstance(token.value, int):
                literal = IntLiteral(value=token.value)
            elif isinstance(token.value, float):
                literal = FloatLiteral(value=token.value)
        elif token.token_type == TokenType.STRING_LITERAL:
            literal = StringLiteral(value=token.value)
        elif token.token_type == TokenType.BOOL_LITERAL:
            value = Literal.BOOLEAN_FILTER.get(token.value)
            literal = BoolLiteral(value=value)
        elif token.token_type == TokenType.NULL_LITERAL:
            literal = NullLiteral()
        else:
            raise Exception(f"Unknown type of literal\n{token}\n")

        self.scanner.next_token()
        return literal

    def is_literal(self, token_type: TokenType) -> bool:
        return  token_type == TokenType.NUMERIC_LITERAL or \
                token_type == TokenType.STRING_LITERAL or \
                token_type == TokenType.BOOL_LITERAL or \
                token_type == TokenType.NULL_LITERAL

    def check_current_token(self, token_type: TokenType, error_msg: str="") -> None:
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

    def must_be_token(self, token_type: TokenType, error_msg: str="") -> None:
        self.check_current_token(token_type, error_msg=error_msg)
        self.scanner.next_token()
