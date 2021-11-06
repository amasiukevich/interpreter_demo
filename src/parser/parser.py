from src.exceptions.parsing_exception import ParsingException
from src.scanner.scanner import Scanner
from src.utils.program3.expressions.math.add_expression import AddExpression
from src.utils.program3.expressions.math.and_expression import AndExpression
from src.utils.program3.expressions.math.equality_expression import EqualityExpression
from src.utils.program3.expressions.math.multiply_expression import MultiplyExpression
from src.utils.program3.expressions.math.negative_unary_expression import NegativeUnaryExpression
from src.utils.program3.expressions.math.not_unary_expression import NotUnaryExpression
from src.utils.program3.expressions.math.or_expression import OrExpression
from src.utils.program3.expressions.math.relation_expression import RelationExpression

from src.utils.program3.expressions.operators.oper_mapper import OperatorMapper
from src.utils.program3.functions.parameters import Parameters


from src.utils.program3.program import Program
from src.utils.program3.functions.function import Function
from src.utils.program3.classes._class import Class
from src.utils.program3.block import Block
from src.utils.program3.functions.arguments import Arguments
from src.utils.program3.functions.argument import Argument
from src.utils.program3.classes.class_block import ClassBlock
from src.utils.program3.statements.comment import Comment
from src.utils.program3.statements.conditional import Conditional
from src.utils.program3.statements.foreach_loop import ForeachLoop
from src.utils.program3.statements._return import Return
from src.utils.program3.statements.reflect import Reflect
from src.utils.program3.statements.rest_function_call import RestFunctionCall
from src.utils.program3.statements.while_loop import WhileLoop
from src.utils.program3.statements.assign import Assign
from src.utils.program3.values.basic_value_getter import BasicValueGetter
from src.utils.program3.values.list_value import ListValue
from src.utils.program3.values.literals.bool_literal import BoolLiteral
from src.utils.program3.values.literals.float_literal import FloatLiteral
from src.utils.program3.values.literals.int_literal import IntLiteral
from src.utils.program3.values.literals.string_literal import StringLiteral
from src.utils.program3.values.no_call_value_getter import NoCallValueGetter
from src.utils.program3.values.rest_value_getter import RestValueGetter

from src.utils.program3.values.this_value_getter import ThisValueGetter
from src.utils.program3.values.complex_value_getter import ComplexValueGetter


from src.utils.token_type import TokenType
from src.utils.token import Token
# TODO: Add type hints to all of the methods


class Parser:

    def __init__(self, scanner: Scanner):

        self.scanner = scanner
        self.scanner.next_token()
        self.token = self.scanner.get_token()

        self.oper_mapper: OperatorMapper= OperatorMapper()

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

        # TODO: Remove DEFINE
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
        if self.compare_token_types(TokenType.IDENTIFIER):

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

            try:

                self.must_be_token(
                    TokenType.CLOSING_CURLY_BRACKET,
                    f"{self.scanner.get_token().position}: Missing closing bracket."
                )

                block = Block(statements=statements)

            except Exception as e:
                breakpoint()
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

        # try parsing conditional
        statement = self.parse_conditional()
        if statement:
            return statement

        # try parsing loops
        statement = self.parse_while_loop()
        if statement:
            return statement

        statement = self.parse_foreach_loop()
        if statement:
            return statement

        # try parsing return
        statement = self.parse_return()
        if statement:
            return statement

        # try parsing comment
        statement = self.parse_comment()
        if statement:
            return statement

        # try parsing reflect
        statement = self.parse_reflect()
        if statement:
            return statement

        # try parsing assign or function call
        statement = self.parse_assign_or_function_call()
        if statement:
            return statement

    def parse_conditional(self):

        if self.compare_and_consume(TokenType.IF):

            conditions = []
            blocks = []

            expression = self.parse_or_expression()

            if_block = self.parse_block()
            conditions.append(expression)
            blocks.append(if_block)

            # multiple elseif blocks
            # TODO: rewrite it without break and continue
            # TODO: check if the parsed components is not None
            while self.compare_and_consume(TokenType.ELSE):

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
                    break

            return Conditional(expressions=conditions, blocks=blocks)

    def parse_while_loop(self):

        # TODO: Check condition and block on nullness
        if self.compare_and_consume(TokenType.WHILE):

            condition = self.parse_or_expression()
            block = self.parse_block()

            while_loop = WhileLoop(condition, block)

            return while_loop

    def parse_foreach_loop(self):

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

    def parse_return(self):

        # TODO: Check returning expression
        if self.compare_and_consume(TokenType.RETURN):

            returning_expression = self.parse_or_expression()
            self.must_be_token(TokenType.SEMICOLON)

            return Return(returning_expression)

    def parse_reflect(self):

        # TODO: Check the expression on nullness
        if self.compare_and_consume(TokenType.REFLECT):

            is_recursive = self.compare_and_consume(TokenType.RECURSIVE)
            expression = self.parse_or_expression()

            self.must_be_token(TokenType.SEMICOLON)


            return Reflect(is_recursive=is_recursive, expression=expression)

    def parse_comment(self):

        if self.compare_token_types(TokenType.COMMENT):
            token = self.scanner.get_token_and_move()
            return Comment(comment_body=token.value)



    def parse_assign_or_function_call(self):

        complex_value_getter = self.parse_complex_value_getter()

        if self.compare_and_consume(TokenType.ASSIGN):
            # Assign statement
            expression = self.parse_or_expression()
            self.must_be_token(TokenType.SEMICOLON)

            assign_statement = Assign(complex_value_getter, expression)
            return assign_statement

        elif self.compare_and_consume(TokenType.SEMICOLON):
            # meaning function call
            return complex_value_getter

    def parse_complex_value_getter(self):

        this_value_getter = None
        if self.compare_and_consume(TokenType.THIS):
            self.must_be_token(TokenType.ACCESS)
            this_value_getter = ThisValueGetter()

        rest_getter = self.parse_rest_value_getter()

        # getting last getter
        last_getter = None
        if rest_getter and len(rest_getter.get_basic_getters()) > 0:
            last_getter = rest_getter.get_basic_getters().pop()
            if len(rest_getter.get_basic_getters()) == 0:
                rest_getter = None

        final_last_getter = None
        if last_getter:

            # no call case
            if not last_getter.get_rest_func_call():
                final_last_getter = NoCallValueGetter(
                    identifier=last_getter.get_identifier(),
                    slicing_expr=last_getter.get_slicing_expr()
                )
            # call case
            else:
                final_last_getter = last_getter

        return ComplexValueGetter(
            this_value_getter=this_value_getter,
            rest_value_getter=rest_getter,
            last_getter=final_last_getter
        )

    def parse_rest_value_getter(self):

        basic_getter = self.parse_basic_value_getter()

        if basic_getter:

            basic_getters = []
            basic_getters.append(basic_getter)

            while self.compare_and_consume(TokenType.ACCESS):
                basic_getter = self.parse_basic_value_getter()
                basic_getters.append(basic_getter)

            return RestValueGetter(base_getters=basic_getters)

    def parse_basic_value_getter(self):

        if self.compare_token_types(TokenType.IDENTIFIER):
            identifier = self.scanner.get_token_and_move()
            rest_func_call = self.parse_rest_function_call()

            slicing_expr = None
            # slicing
            if self.compare_and_consume(TokenType.OPEN_BRACKET):
                slicing_expr = self.parse_or_expression()
                self.must_be_token(TokenType.CLOSING_BRACKET)

            return BasicValueGetter(
                identifier=identifier,
                rest_function_call=rest_func_call,
                slicing_expr=slicing_expr
            )

    def parse_rest_function_call(self):

        if self.compare_and_consume(TokenType.OPEN_PARENTHESIS):

            arguments = None
            arguments = self.parse_arguments()

            self.must_be_token(TokenType.CLOSING_PARENTHESIS)

            return RestFunctionCall(arguments)

    def parse_arguments(self):

        list_of_args = []
        argument = self.parse_argument()
        if argument:
            list_of_args.append(argument)
            while self.compare_and_consume(TokenType.COMMA):

                argument = self.parse_argument()
                list_of_args.append(argument)

        return Arguments(arguments=list_of_args)

    def parse_argument(self):

        is_by_ref = False

        if self.compare_and_consume(TokenType.BY_REF):
            is_by_ref = True

        expression = self.parse_or_expression()

        return Argument(is_by_ref=is_by_ref, expression=expression)
    # TODO: refactor the expressions after tests!!!
    # def parse_expression(self,
    #                      current_expr_class: Expression = None,
    #                      level_down_expr_class: Expression = None,
    #                      level_down_parser=None):
    #
    #     expression_components = []
    #     downgrade_expression = level_down_parser()
    #     pass

    def parse_or_expression(self):

        expression_components = []

        and_expression = self.parse_and_expression()
        if and_expression:

            expression_components.append(and_expression)

            while self.compare_and_consume(TokenType.OR):
                and_expression = self.parse_and_expression()

                # TODO: Custom exception there
                if not and_expression:
                    raise Exception("Error while parsing OR Expression")

                expression_components.append(and_expression)

        if len(expression_components) == 1:
            return and_expression

        return OrExpression(expressions=expression_components)

    def parse_and_expression(self):

        expression_components = []
        eq_expression = self.parse_eq_expression()

        if eq_expression:

            expression_components.append(eq_expression)

            while self.compare_and_consume(TokenType.AND):
                eq_expression = self.parse_eq_expression()

                # TODO: Custom exception here
                if not eq_expression:
                    raise Exception("Error while parsing AND Expression")

                expression_components.append(eq_expression)
        if len(expression_components) == 1:
            return eq_expression

        return AndExpression(expressions=expression_components)

    def parse_eq_expression(self):

        expression_components = []
        operators = []
        rel_expression = self.parse_rel_expression()

        if rel_expression:

            expression_components.append(rel_expression)

            while self.is_eq_token():

                operator = self.parse_operator()

                # TODO: Custom exception here
                if not operator:
                    raise Exception("Error while parsing operator in equality expression")
                operators.append(operator)

                rel_expression = self.parse_rel_expression()

                # TODO: Custom exception here
                if not rel_expression:
                    raise Exception("Error while parsing Equality Expression")
                expression_components.append(rel_expression)

        if len(expression_components) == 1:
            return rel_expression

        return EqualityExpression(
            expressions=expression_components,
            operators=operators
        )

    def is_eq_token(self):
        token_type = self.scanner.get_token().token_type
        return token_type == TokenType.EQUAL or \
               token_type == TokenType.NOT_EQUAL

    def parse_rel_expression(self):

        expression_components = []
        operators = []

        add_expression = self.parse_add_expression()

        if add_expression:

            expression_components.append(add_expression)

            while self.is_rel_token():

                operator = self.parse_operator()

                # TODO: custom exception here
                if not operator:
                    raise Exception("Error while parsing operator relation expression")
                operators.append(operator)

                add_expression = self.parse_rel_expression()

                # TODO: Custom exception here
                if not add_expression:
                    raise Exception("Error while parsing Relation Expression")
                expression_components.append(add_expression)

        if len(expression_components) == 1:
            return add_expression

        return RelationExpression(
            expressions=expression_components,
            operators=operators
        )

    def is_rel_token(self):
        token_type = self.scanner.get_token().token_type
        return token_type == TokenType.GREATER or \
               token_type == TokenType.GREATER_EQUAL or \
               token_type == TokenType.LESS or \
               token_type == TokenType.LESS_EQUAL

    def parse_add_expression(self):

        expression_components = []
        operators = []

        mult_expression = self.parse_mult_expression()

        if mult_expression:

            expression_components.append(mult_expression)

            while self.is_add_token():

                operator = self.parse_operator()

                # TODO: Custom exception here
                if not operator:
                    raise Exception("Error while parsing operator additive expression")
                operators.append(operator)

                mult_expression = self.parse_mult_expression()

                # TODO: Custom exception here
                if not mult_expression:
                    raise Exception("Error while parsing additive expression")
                expression_components.append(mult_expression)

        if len(expression_components) == 1:
            return mult_expression

        return AddExpression(
            expressions=expression_components,
            operators=operators
        )

    def is_add_token(self):
        token_type = self.scanner.get_token().token_type
        return token_type == TokenType.PLUS or \
               token_type == TokenType.MINUS

    def parse_mult_expression(self):

        expression_components = []
        operators = []

        unary_expression = self.parse_unary_expression()

        if unary_expression:
            expression_components.append(unary_expression)

            while self.is_mult_token():

                operator = self.parse_operator()
                # TODO: Custom Exception here
                if not operator:
                    raise Exception("Error while parsing operator in multiply expression")
                operators.append(operator)

                unary_expression = self.parse_unary_expression()

                # TODO: Custom exception here
                if not unary_expression:
                    raise Exception("Error while parsing unary expression")
                expression_components.append(unary_expression)


        if len(expression_components) == 1:
            return unary_expression

        return MultiplyExpression(
            expressions=expression_components,
            operators=operators
        )

    def is_mult_token(self):
        token_type = self.scanner.get_token().token_type
        return token_type == TokenType.MULTIPLY or \
               token_type == TokenType.DIVIDE or \
               token_type == TokenType.MODULO

    def parse_unary_expression(self):

        not_expression = self.parse_not_unary_expression()
        if not_expression:
            return not_expression

        neg_expression = self.parse_negative_unary_expression()
        if neg_expression:
            return neg_expression

        general_value = self.parse_general_value()
        if general_value:
            return general_value

    def parse_not_unary_expression(self):

        if self.compare_and_consume(TokenType.NOT):
            expression = self.parse_unary_expression()
            not_unary_expression = NotUnaryExpression(expression)

            return not_unary_expression

    def parse_negative_unary_expression(self):

        if self.compare_and_consume(TokenType.MINUS):
            expression = self.parse_unary_expression()
            neg_unary_expression = NegativeUnaryExpression(expression)

            return neg_unary_expression

    def parse_general_value(self):

        if self.compare_and_consume(TokenType.OPEN_PARENTHESIS):

            or_expression = self.parse_or_expression()
            self.must_be_token(TokenType.CLOSING_PARENTHESIS)

            return or_expression
        else:
            return self.parse_value()


    def parse_operator(self):

        token_type = self.scanner.get_token().token_type

        operator = self.oper_mapper.token_to_operator.get(token_type)
        additive_operator = self.oper_mapper.token_to_operator_additive.get(token_type)
        if operator:
            self.scanner.next_token()
            return operator
        elif additive_operator:
            self.scanner.next_token()
            return additive_operator

    def parse_value(self):

        token = self.scanner.get_token()
        value = None

        # literal case
        if self.is_literal(token.token_type):
            value = self.token_to_literal(token)
        # list value
        elif self.compare_and_consume(TokenType.OPEN_BRACKET):

            list_value = self.parse_list_value()
            self.must_be_token(TokenType.CLOSING_BRACKET)
            value = list_value
        # complex value getter
        elif self.compare_token_types(TokenType.IDENTIFIER) or self.compare_token_types(TokenType.THIS):
            value = self.parse_complex_value_getter()

        return value

    def parse_list_value(self):

        component_expressions = []
        or_expression = self.parse_or_expression()
        if or_expression:
            component_expressions.append(or_expression)

        while self.compare_and_consume(TokenType.COMMA):
            or_expression = self.parse_or_expression()

            if not or_expression:
                raise Exception("Wrong expression in the list")
            component_expressions.append(or_expression)

        return ListValue(expressions=component_expressions)

    def token_to_literal(self, token: Token):

        literal = None
        if token.token_type == TokenType.NUMERIC_LITERAL:
            if isinstance(token.value, int):
                literal = IntLiteral(value=token.value)
            elif isinstance(token.value, float):
                literal = FloatLiteral(value=token.value)
        elif token.token_type == TokenType.STRING_LITERAL:
            literal = StringLiteral(value=token.value[1:-1])
        elif token.token_type == TokenType.BOOL_LITERAL:
            literal = BoolLiteral(value=token.value)
        else:
            raise Exception(f"Unknown type of literal\n{token}\n")

        self.scanner.next_token()
        return literal

    def is_literal(self, token_type: TokenType):
        return token_type == TokenType.NUMERIC_LITERAL or \
               token_type == TokenType.STRING_LITERAL or \
               token_type == TokenType.BOOL_LITERAL

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
