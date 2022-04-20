import typing
from typing import Optional

from src.exceptions import InterpretingException, RuntimeException
from src.utils.interpreter_utils.peramolang_callable import PeramolangCallable, NativeFunction, PeramolangFunction, \
    ReturnObj
from src.utils.program3.classes._class import Class
from src.utils.program3.expressions.expression import Expression
from src.utils.program3.expressions.math.add_expression import AddExpression
from src.utils.program3.expressions.math.and_expression import AndExpression
from src.utils.program3.expressions.math.equality_expression import EqualityExpression
from src.utils.program3.expressions.math.multiply_expression import MultiplyExpression
from src.utils.program3.expressions.math.or_expression import OrExpression
from src.utils.program3.expressions.math.relation_expression import RelationExpression
from src.utils.program3.expressions.math.unary_expression import UnaryExpression
from src.utils.program3.functions.function import Function
from src.utils.program3.statements._return import Return
from src.utils.program3.statements.assign import Assign
from src.utils.program3.statements.comment import Comment
from src.utils.program3.statements.conditional import Conditional
from src.utils.program3.statements.foreach_loop import ForeachLoop
from src.utils.program3.statements.func_call import FunctionCall
from src.utils.program3.statements.rest_function_call import RestFunctionCall
from src.utils.program3.statements.statement import Statement
from src.utils.program3.statements.while_loop import WhileLoop
from src.utils.program3.values.complex_getter import ComplexGetter
from src.utils.program3.values.literals.literal import Literal

from src.utils.program3.variable import Variable
from src.utils.visitor_old import Visitor

from src.utils.interpreter_utils.environment import Environment, DummyEnvironment


from src.utils.program3.expressions.operators import *


class Interpreter(Visitor):

    # TODO: handle print function to known from the beginning (Add it to the program's functions?)

    def __init__(self, program, start_function="main"):

        self.program = program
        self.start_function = start_function
        # self.globals = Environment()
        # self.environment = Environment()

        globals = DummyEnvironment()
        self.environment = globals
        self.init_native_functions()

        # TODO: maybe add here print stream???

        self.had_runtime_error = False

    def init_native_functions(self):

        def call_method(arguments):
            string = str(arguments[0])
            print(string)

        print_func = NativeFunction(call_func=call_method, arity=1)
        self.environment.define("print", print_func)

    def execute(self):
        self.program.accept(self)

    def visit_program(self, program):

        # find the function to start from
        main_function = program.get_function(self.start_function)
        if not main_function:
            raise InterpretingException('Function to start from not found')

        if len(main_function.get_params()) != 0:
            raise InterpretingException('Starting function should not contain any arguments')

        main_function.accept(self)
        main_function_obj = self.environment.get_variable_or_function('main')
        # Symulating function call here
        try:
            main_function_obj.call(interpreter=self, arguments=None)
        except RuntimeException as e:
            print(e.message)
            # raise RuntimeException(message=f"Couldn't load {main_function.identifier} function")


        # self.environment.push_new_fcc()
        # main_function.accept(self)
        # self.environment.pop_fcc()


    def visit_function(self, function: Function):

        peramolang_function = PeramolangFunction(function)
        self.environment.define(function.identifier, peramolang_function)

    def visit_class(self, _class: Class):
        pass

    def visit_parameters(self, parameters):

        # TODO: Maybe modify parser such that function contains info if it's a method
        if parameters.has_this:
            # TODO: Inform function somehow
            pass

        param_names = parameters.get_param_names()

        for name in param_names:
            self.environment.add_variable(Variable(name=name))

    # def set_parameter_values(self, parameters):
    #
    #     # TODO: What's with the methods???
    #     param_names = parameters.get_param_names()
    #     pass

    # TODO: Statements:
    def visit_statement(self, statement: Statement):
        statement.accept(self)

    def visit_return(self, _return: Return):
        # TODO: Implement return without throwing an exception
        value = None
        if _return.expression:
            value = _return.expression.accept(self)
        raise ReturnObj(value=value)

    # TODO: Very dummy for now (assigning first-level variables)
    def visit_assign(self, assign: Assign):

        value = self.visit_or_expression(assign.expression)

        # Simple variable case (creation and redefinition)
        self.environment.define(
            assign.complex_getter.get_last_getter().identifier,
            value
        )

        # TODO: more complex case with getters, this, etc...

        # last_getter = assign.value_getter.get_last_getter()
        # if not last_getter.get_rest_funct_call():
        #     name = last_getter.get_identifier()
        #     value = assign.expression.accept(self)
        #
        #     self.environment.add_variable(name, value)
        # else:
        #     raise RuntimeException("Assign statement requires initializer")

    def visit_comment(self, comment: Comment):
        pass

    # TODO: Suggestion - make expressions and blocks a dictionary
    def visit_conditional(self, conditional: Conditional):
        matched_condition = False
        for i, expression in enumerate(conditional.expressions):
            if  matched_condition := self.is_truthy(expression.accept(self)):
                conditional.blocks[i].accept(self)
                break
        if not matched_condition and not conditional.is_single_if():
            conditional.blocks[-1].accept(self)

    def visit_foreach_loop(self, foreach_loop: ForeachLoop):
        # TODO: Add a collection to your language to do this
        pass

    def visit_rest_function_call(self, rest_function_call: RestFunctionCall):
        pass

    def visit_while_loop(self, while_loop: WhileLoop):
        while self.is_truthy(while_loop.expression.accept(self)):
            while_loop.block.accept(self)

    # TODO: Create a print statement in scanner and parser
    def visit_print(self):
        pass


    # VALUES

    # TODO: add scope to call context every time entering the block
    # TODO: remove scope from call context every time returning from the block

    # TODO: dummy
    def visit_function_call(self, function_call: FunctionCall):

        # TODO: function call and class instance should inherit after PeramolangCallable
        callee_name = function_call.get_callee_name()
        callee = self.environment.get_variable_or_function(callee_name)

        # list of arguments
        arguments = []
        for argument in function_call.get_arguments():
            arguments.append(
                argument.accept(self)
            )

        if not isinstance(callee, PeramolangCallable):
            raise RuntimeException("Can only call functions and classes")

        # TODO: get_arity is the number of function PARAMETERS
        if len(arguments) != callee.get_arity():
            raise RuntimeException(f"Expected {callee.get_arity()}, but found {len(arguments)}.")

        return callee.call()


    def visit_arguments(self, arguments):
        pass

    # Statements and control flow

    def visit_block(self, block):

        new_env = DummyEnvironment(enclosing=self.environment)
        self.execute_block(block, new_env)

    def visit_class_block(self, class_block):
        pass

    def execute_block(self, block, environment):

        previous_env = self.environment
        try:
            self.environment = environment
            for statement in block.statements:
                statement.accept(self)
        finally:
            self.environment = previous_env

    # TODO: make it no dummy (classes)
    def visit_complex_getter(self, complex_getter: ComplexGetter):
        return self.environment.get_variable_or_function(complex_getter.get_last_getter().get_identifier())

    def visit_iterative_getter(self):
        pass

    # ARITHMETIC AND LOGIC
    def visit_or_expression(self, or_expression: OrExpression):

        if isinstance(or_expression, OrExpression):
            return self.evaluate_logical_expression(or_expression)
        else:
            return self.visit_and_expression(or_expression)

    def visit_and_expression(self, and_expression: AndExpression):
        if isinstance(and_expression, AndExpression):
            return self.evaluate_logical_expression(and_expression)
        else:
            return self.visit_eq_expression(and_expression)


    def evaluate_logical_expression(self, expression: Expression):

        if isinstance(expression, Literal):
            return self.is_truthy(expression)

        for i in range(len(expression.expressions) - 1):
            subexpression = expression.expressions[i]
            sub_result = subexpression.accept(self)
            if isinstance(expression, OrExpression):
                if self.is_truthy(sub_result):
                    return sub_result
            elif isinstance(expression, AndExpression):
                if not self.is_truthy(sub_result):
                    return sub_result

        return expression.expressions[-1].accept(self)

    # Evaluating expressions
    def visit_eq_expression(self, eq_expression):
        if isinstance(eq_expression, EqualityExpression):
            left_expr = eq_expression.expressions[0].accept(self)
            right_expr = eq_expression.expressions[1].accept(self)
            operator = eq_expression.operator

            if isinstance(operator, EqualityOperator):
                return left_expr == right_expr
            elif isinstance(operator, NotEqualOperator):
                return left_expr != right_expr
        else:
            return self.visit_rel_expression(eq_expression)

    def visit_rel_expression(self, rel_expression):

        if isinstance(rel_expression, RelationExpression):
            left_expr = rel_expression.expressions[0].accept(self)
            right_expr = rel_expression.expressions[1].accept(self)

            operator = rel_expression.operator

            if self.is_comparable(left_expr, right_expr):
                if isinstance(operator, LessOperator):
                    return left_expr < right_expr
                elif isinstance(operator, LessEqualOperator):
                    return left_expr <= right_expr
                elif isinstance(operator, GreaterOperator):
                    return left_expr > right_expr
                elif isinstance(operator, GreaterEqualOperator):
                    return left_expr >= right_expr
        else:
            return self.visit_add_expression(rel_expression)

    # binary expressions
    def visit_add_expression(self, add_expression):
        try:
            if isinstance(add_expression, AddExpression):
                final_result = add_expression.expressions[0].accept(self)
                for i in range(1, len(add_expression.expressions)):

                    right_expr_val = add_expression.expressions[i].accept(self)
                    curr_operator = add_expression.operators[i - 1]

                    if isinstance(curr_operator, PlusOperator):

                        if isinstance(final_result, str) and isinstance(right_expr_val, str):
                            final_result = final_result + right_expr_val

                        elif any([isinstance(final_result, cls) for cls in [int, float]]) and \
                            any([isinstance(right_expr_val, cls) for cls in [int, float]]):

                            final_result, right_expr_val = self.apply_add_casting(final_result, right_expr_val)
                            final_result = final_result + right_expr_val
                        else:
                            raise RuntimeException(token=None, message='Operands must be either two numbers or two strings')

                    elif isinstance(curr_operator, MinusOperator):
                        self.check_number_operands(final_result, right_expr_val)
                        final_result -= right_expr_val

                return final_result
            else:
                return self.visit_mult_expression(add_expression)
        except Exception as e:
            print("Hi there")

    def visit_mult_expression(self, mult_expression):

        if isinstance(mult_expression, MultiplyExpression):

            final_result = mult_expression.expressions[0].accept(self)
            for i in range(1, len(mult_expression.expressions)):

                right_expr_val = mult_expression.expressions[i].accept(self)
                curr_operator = mult_expression.operators[i - 1]

                self.check_number_operands(final_result, right_expr_val)

                if isinstance(curr_operator, MultiplyOperator):
                    final_result *= right_expr_val
                elif isinstance(curr_operator, DivideOperator):
                    if final_result == 0:
                        # TODO: How to show user the context of an error???
                        raise RuntimeException("Zero Division Error")
                    else:
                        final_result %= right_expr_val
                elif isinstance(curr_operator, ModuloOperator):
                    if final_result == 0:
                        # TODO: How to show user the context of an error???
                        raise RuntimeException("Zero Division Error")
                    else:
                        final_result %= right_expr_val

            return final_result
        else:
            return self.visit_unary_expression(mult_expression)


    # unary expression
    def visit_unary_expression(self, unary_expression: UnaryExpression):

        if isinstance(unary_expression, Literal):
            expr_value = self.visit_literal(unary_expression)
            return expr_value
        elif isinstance(unary_expression, Variable):
            pass
        else:
            expr_value = unary_expression.expression.accept(self)
            if isinstance(unary_expression.operator, NegativeOperator):
                self.check_number_operand(expr_value)
                return -expr_value
            elif isinstance(unary_expression.operator, NotOperator):
                self.check_bool_operand(unary_expression)
                return not bool(expr_value)
            else:
                return None

    def visit_literal(self, literal: Literal):
        return literal.value

    def visit_variable(self, variable: Variable):
        return self.environment.get_variable_or_function(variable.name)


    # TODO: Create a place for those utility function (maybe separate file/module???)
    def apply_add_casting(self, val1, val2):

        if isinstance(val1, float) or isinstance(val2, float):
            val1, val2 = float(val1), float(val2)
        else:
            val1, val2 = int(val1), int(val2)

        return val1, val2

    def is_comparable(self, val1, val2):
        if isinstance(val1, bool) and isinstance(val1, bool):
            return False
        elif any([isinstance(item, str) for item in [val1, val2]]) and \
            not all([isinstance(item, str) for item in [val1, val2]]):

            return False
        else:
            return True

    def check_number_operand(self, operand):
        if not any([isinstance(operand, num) for num in [int, float]]):
            # TODO: How to show user the context of an error???
            raise RuntimeException("Operand must be a number")

    def check_bool_operand(self, operand):
        if not isinstance(operand, bool):
            raise RuntimeException("Operand must be boolean")

    def check_number_operands(self, operand_left, operand_right):
        if any([isinstance(operand_left, cls) for cls in [int, float]]) and \
            any([isinstance(operand_right, cls) for cls in [int, float]]):
            return
        raise RuntimeException("Operand must be a number")

    def is_truthy(self, expression):
        if not expression:
            return False
        if isinstance(expression, bool):
            return expression
        else:
            return True