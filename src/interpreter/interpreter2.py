from typing import List, Tuple

### Program Tree
from src.utils.program3.program import Program
from src.utils.program3.functions.function import Function
from ..utils.interpreter2_utils.call_utils import NativeFunction
from ..utils.program3.block import Block
from ..utils.program3.classes._class import Class
from ..utils.program3.classes.class_block import ClassBlock
from ..utils.program3.expressions.math.add_expression import AddExpression
from ..utils.program3.expressions.math.and_expression import AndExpression
from ..utils.program3.expressions.math.equality_expression import EqualityExpression
from ..utils.program3.expressions.math.multiply_expression import MultiplyExpression
from ..utils.program3.expressions.math.or_expression import OrExpression
from ..utils.program3.expressions.math.relation_expression import RelationExpression
from ..utils.program3.expressions.math.unary_expression import UnaryExpression
from ..utils.program3.expressions.operators import PlusOperator, MinusOperator, MultiplyOperator, DivideOperator, \
    ModuloOperator, EqualityOperator, GreaterEqualOperator, GreaterOperator, LessOperator, LessEqualOperator, \
    NotOperator, NotEqualOperator
from ..utils.program3.functions.arguments import Arguments
from ..utils.program3.functions.parameters import Parameters
from ..utils.program3.statements._return import Return
from ..utils.program3.statements.assign import Assign
from ..utils.program3.statements.conditional import Conditional
from ..utils.program3.statements.func_call import FunctionCall
from ..utils.program3.statements.while_loop import WhileLoop
from src.utils.program3.statements.complex_getter import ComplexGetter
from ..utils.program3.values.iterative_getter import CallGetter, IdentifierGetter
from ..utils.program3.values.literals.bool_literal import BoolLiteral
from ..utils.program3.values.literals.float_literal import FloatLiteral
from ..utils.program3.values.literals.int_literal import IntLiteral
from ..utils.program3.values.literals.literal import Literal
from ..utils.program3.values.literals.null_literal import NullLiteral
from ..utils.program3.values.literals.string_literal import StringLiteral
from ..utils.program3.variable import Variable
from ..utils.program3.statements.comment import Comment
from ..utils.interpreter2_utils.instance import Instance

from src.utils.visitor import Visitor
from src.utils.interpreter2_utils.environment import Environment
from src.exceptions import RuntimeException, ArithmeticException


# TODO: rewrite iterative getter to support polymorphism (function_call, identifier, slicing_expr)


class Interpreter(Visitor):

    def __init__(self, program: Program, start_function: str):
        # the root of AST tree
        self.program = program
        self.main_func_name = start_function
        self.environment = Environment()

        self.move_program_objects()

    def execute(self):
        self.program.accept(self)

    def move_program_objects(self):

        for func_name, func_obj in self.program.function_dict.items():
            self.environment.add_variable(Variable(name=func_name, value=func_obj))

        for cls_name, cls_obj in self.program.class_dict.items():
            self.environment.add_variable(Variable(name=cls_name, value=cls_obj))

    def visit_program(self, program: Program):
        # find main function
        # main_function = self.program.get_function(self.main_func_name)

        main_function = self.environment.get_variable(self.main_func_name).value

        if not main_function:
            raise RuntimeException(message=f"No starting function named: {self.main_func_name}")
        if len(main_function.get_params()) != 0:
            raise RuntimeException(message=f"{self.main_func_name} should have exactly 0 parameters "
                                           f"to be a starting function")

        # TODO: moving all of the functions to the current environment

        # interpreting main
        main_function.accept(self)

    def visit_function(self, function: Function):

        function.block.accept(self)
        # TODO: return stuff here

    def visit_class(self, _class: Class, constructor_params: List):

        # TODO: Create the constructor recognizable
        instance = Instance(klass=_class)
        for value in constructor_params:
            instance.constructor_params.append(value)

        _class.class_block.accept(self, instance)

    def visit_parameters(self, parameters: Parameters):

        param_names = parameters.get_param_names()
        for name in param_names:
            variable = Variable(name=name, value=None)
            self.environment.add_variable(variable)

    def set_parameter_values(self, evaluated_args: List, param_names: List[str]):

        for arg, param_name in zip(evaluated_args, param_names):
            variable = self.environment.get_variable(param_name)
            if not variable:
                variable = Variable(name=param_name, value=arg)
            else:
                variable.value = arg
            variable.accept(self)

    def visit_block(self, block: Block):

        if self.environment.get_returned()[0]:
            return

        self.environment.push_scope()
        for statement in block.get_statements():
            statement.accept(self)
            if self.environment.get_returned()[0]:
                return
            # TODO: interrupt the block if returned
        self.environment.pop_scope()

    def visit_class_block(self, class_block: ClassBlock, instance: Instance):

        constructor = instance.klass.get_constructor()

        # TODO: add here attributes
        # TODO: add here rec_attributes

        self.environment.push_scope(instance.scope)
        instance.scope.add_variable(Variable(name='this', value=instance))
        for method in class_block.methods:
            if method != constructor:
                function = Variable(method.identifier, method)
                instance.scope.add_variable(function)

        # call constructor here
        # TODO: Somewhere here is the error
        args = [instance] + instance.constructor_params
        params = ['this'] + constructor.get_param_names()
        self.set_parameter_values(evaluated_args=args, param_names=params)
        constructor.accept(self)
        self.environment.set_returned(fact=True, value=instance)
        self.environment.pop_scope()

    def visit_function_call(self, function_call):
        pass

    def visit_native_function(self, native_function: NativeFunction, evaluated_args: List):
        val = native_function.call_func(*evaluated_args)
        return val

    def visit_assign(self, assign: Assign):

        # right part
        right_val = assign.expression.accept(self)

        # left_part
        assign.complex_getter.accept(self, is_assign=(True, right_val))

    # Statements
    # def visit_assign(self, assign: Assign):
    #
    #     # if self.environment.is_returned:
    #     #     return
    #
    #     assign.expression.accept(self)
    #     right_value = self.environment.pop_value()
    #
    #     # left part
    #     env = self.environment
    #     last_getter_idx = len(assign.complex_getter.iterative_getters) - 1
    #     for i, it_getter in enumerate(assign.complex_getter.iterative_getters):
    #
    #         if isinstance(it_getter, IdentifierGetter):
    #             var = env.get_variable(it_getter.get_identifier())
    #             if var:
    #                 if i != last_getter_idx and isinstance(var.value, Instance):
    #                     env = var.value.environment
    #                 else:
    #                     var.set_value(right_value)
    #             else:
    #                 if i == last_getter_idx:
    #                     variable = Variable(name=it_getter.get_identifier(), value=right_value)
    #                     tmp_env, self.environment = self.environment, env
    #                     variable.accept(self)
    #                     self.environment = tmp_env
    #                 else:
    #                     # TODO: get there fancy message about not found attribute in object
    #                     raise RuntimeException(message=f"Object has no attribute {it_getter.get_identifier()}")
    #         elif isinstance(it_getter, CallGetter):
    #             call_complex_getter = ComplexGetter(has_this=assign.complex_getter.has_this)
    #             function_call_obj = FunctionCall(call_complex_getter)
    #             tmp_env, self.environment = self.environment, env
    #             function_call_obj.accept(self)
    #
    #             result = self.environment.pop_value()
    #             self.environment = tmp_env
    #             if i != last_getter_idx:
    #                 if isinstance(result, Instance):
    #                     env = result.environment
    #                 else:
    #                     raise Exception("Function call doesn't evaluate to object")
    #             else:
    #                 raise Exception("Cannot assign to function call")

    def visit_return(self, _return: Return):

        if expression := _return.expression:
            value = expression.accept(self)
            self.environment.set_returned(fact=True, value=value)
        else:
            self.environment.set_returned(True)

    def visit_while_loop(self, while_loop: WhileLoop):

        condition, body = while_loop.expression, while_loop.block
        condition_value = condition.accept(self).value
        try:

            while condition_value and not self.environment.get_returned()[0]:
                body.accept(self)
                condition_value = condition.accept(self).value
        except Exception as e:
            print("Hey there")

    def visit_conditional(self, conditional: Conditional):

        block_chosen = False
        for i, condition in enumerate(conditional.expressions):

            condition_value = condition.accept(self)

            if condition_value.value:
                conditional.blocks[i].accept(self)
                block_chosen = True
                break

        # else case
        if not block_chosen and not conditional.is_single_if():
            conditional.blocks[-1].accept(self)

    # TODO: refactorize these 2 methods (logical)
    def visit_or_expression(self, or_expression: OrExpression):

        left_value = or_expression.expressions[0].accept(self)
        for i in range(1, len(or_expression.expressions)):
            expression = or_expression.expressions[i]
            right_value = expression.accept(self) # TODO: maybe some casting here
            left_value = BoolLiteral(left_value.value or right_value.value)

        return left_value

    def visit_and_expression(self, and_expression: AndExpression):

        left_value = and_expression.expressions[0].accept(self)
        for i in range(1, len(and_expression.expressions)):
            expression = and_expression.expressions[i]
            right_value = expression.accept(self)  # TODO: maybe some casting here
            left_value = BoolLiteral(left_value.value and right_value.value)

        return left_value

    def visit_eq_expression(self, eq_expression: EqualityExpression):

        # evaluating expressions
        left_value = eq_expression.expressions[0].accept(self)
        right_value = eq_expression.expressions[1].accept(self)

        result = eq_expression.operator.accept(self, left_value, right_value)
        return result

    def visit_rel_expression(self, rel_expression: RelationExpression):
        try:
            left_value = rel_expression.expressions[0].accept(self)
            right_value = rel_expression.expressions[1].accept(self)

            result = rel_expression.operator.accept(self, left_value, right_value)
            return result
        except:
            print("Hey there")

    def visit_add_expression(self, add_expression: AddExpression):

        left_value = add_expression.expressions[0].accept(self)
        for i in range(1, add_expression.get_num_expressions()):
            right_value = add_expression.expressions[i].accept(self)
            current_oper = add_expression.operators[i - 1]
            left_value = current_oper.accept(self, left_value, right_value)
        return left_value

    def visit_mult_expression(self, mult_expression: MultiplyExpression):

        left_value = mult_expression.expressions[0].accept(self)
        for i in range(1, mult_expression.get_num_expressions()):
            right_value = mult_expression.expressions[i].accept(self)
            current_oper = mult_expression.operators[i - 1]
            left_value = current_oper.accept(self, left_value, right_value)

        return left_value

    def visit_unary_expression(self, unary_expression: UnaryExpression):

        value = unary_expression.expression.accept(self)
        if unary_expression.operator:
            value = unary_expression.operator.accept(self, value)

        return value

    # TODO: later refactor all of the methods
    def visit_equal_oper(self, eq_oper: EqualityOperator, left_value, right_value):
        return BoolLiteral(left_value.value == right_value.value)

    def visit_not_equal_oper(self, not_eq_oper: NotEqualOperator, left_value, right_value):
        return BoolLiteral(left_value.value != right_value.value)

    def visit_not_oper(self, not_oper: NotOperator, expr):
        return BoolLiteral(not expr.value)

    def visit_greater_oper(self, gt_oper: GreaterOperator, left_value, right_value):
        return BoolLiteral(left_value.value > right_value.value)

    def visit_greater_equal_oper(self, ge_oper: GreaterEqualOperator, left_value, right_value):
        return BoolLiteral(left_value.value >= right_value.value)

    def visit_less_oper(self, lt_oper: LessOperator, left_value, right_value):
        return BoolLiteral(left_value.value < right_value.value)

    def visit_less_equal_oper(self, le_oper: LessEqualOperator, left_value, right_value):
        return BoolLiteral(left_value.value <= right_value.value)

    def visit_plus_oper(self, plus_operator: PlusOperator, left_value, right_value):

        left_literal, right_literal = left_value, right_value
        result = None
        if isinstance(left_literal, StringLiteral) or isinstance(right_literal, StringLiteral):
            result_val = str(left_literal.value) + str(right_literal.value)
            result = StringLiteral(value=result_val)

        elif any([isinstance(left_literal, cls) for cls in [IntLiteral, FloatLiteral]]) or \
                any([isinstance(right_literal, cls) for cls in [IntLiteral, FloatLiteral]]):
            result_val = left_literal.value + right_literal.value
            if isinstance(result_val, int):
                result = IntLiteral(value=result_val)
            elif isinstance(result_val, float):
                result = FloatLiteral(value=result_val)
        elif not result:
            exc_message = f"Cannot add operands of types {type(left_literal)} and {type(right_literal)}"
            raise RuntimeException(message=exc_message)

        return result


    # TODO: Change later literal -> value in the code
    def visit_minus_oper(self, minus_operator: MinusOperator, left_value, right_value):

        left_literal, right_literal = left_value, right_value
        result = None
        if any([isinstance(left_literal, cls) for cls in [IntLiteral, FloatLiteral]]) and \
                any([isinstance(left_literal, cls) for cls in [IntLiteral, FloatLiteral]]):

            result_val = left_literal.value - right_literal.value
            if isinstance(result_val, int):
                result = IntLiteral(value=result_val)
            elif isinstance(result_val, float):
                result = FloatLiteral(value=result_val)
        elif not result:
            exc_message = f"Cannot substract operands of types {type(left_literal)} and {type(right_literal)}"
            raise RuntimeException(message=exc_message)

        return result

    def visit_multiply_oper(self, mult_operator: MultiplyOperator, left_value, right_value):

        left_literal, right_literal = left_value, right_value

        result = None
        if any([isinstance(left_literal, cls) for cls in [IntLiteral, FloatLiteral]]) and \
                any([isinstance(left_literal, cls) for cls in [IntLiteral, FloatLiteral]]):

            result_val = left_literal.value * right_literal.value

            if isinstance(result_val, int):
                result = IntLiteral(value=result_val)
            elif isinstance(result_val, float):
                result = FloatLiteral(value=result_val)

        elif not result:
            exc_message = f"Cannot multiply operands of types {type(left_literal)} and {type(right_literal)}"
            raise RuntimeException(message=exc_message)

        return result

    def visit_divide_oper(self, div_operator: DivideOperator, left_value, right_value):

        left_literal, right_literal = left_value, right_value

        result = None

        if right_literal.value == 0:
            raise ArithmeticException("Division by zero")

        if any([isinstance(left_literal, cls) for cls in [IntLiteral, FloatLiteral]]) and \
                any([isinstance(left_literal, cls) for cls in [IntLiteral, FloatLiteral]]):

            result_val = left_literal.value / right_literal.value

            if isinstance(result_val, int):
                result = IntLiteral(value=result_val)
            elif isinstance(result_val, float):
                result = FloatLiteral(value=result_val)

        elif not result:
            exc_message = f"Cannot divide operands of types {type(left_literal)} and {type(right_literal)}"
            raise RuntimeException(message=exc_message)

        return result

    def visit_modulo_oper(self, modulo_operator: ModuloOperator, left_value, right_value):

        left_literal, right_literal = left_value, right_value

        result = None

        if right_literal.value == 0:
            raise ArithmeticException("Division by zero")

        if any([isinstance(left_literal, cls) for cls in [IntLiteral, FloatLiteral]]) and \
                any([isinstance(left_literal, cls) for cls in [IntLiteral, FloatLiteral]]):

            result_val = left_literal.value % right_literal.value

            if isinstance(result_val, int):
                result = IntLiteral(value=result_val)
            elif isinstance(result_val, float):
                result = FloatLiteral(value=result_val)

        elif not result:
            exc_message = f"Cannot perform modulo operation on operands of types {type(left_literal)} and {type(right_literal)}"
            raise RuntimeException(message=exc_message)

        return result

    def visit_literal(self, literal: Literal):
        return literal

    def visit_complex_getter(self, complex_getter: ComplexGetter, is_assign: Tuple):

        # TODO: Think about when to release scopes
        n_scopes_release = 0
        last_getter_idx = len(complex_getter.iterative_getters) - 1
        scope_to_push = None
        to_return = None
        for i, getter in enumerate(complex_getter.iterative_getters):
            if isinstance(getter, IdentifierGetter):
                var = getter.accept(self)
                if var:
                    var_name, var_value = var.name, var.value
                    if i == last_getter_idx:
                        if is_assign[0]:
                            var.value = is_assign[1]
                            var.accept(self)
                        else:
                            to_return = var_value
                        self.environment.release_scopes(n_scopes=n_scopes_release)
                    else:
                        if isinstance(var_value, Instance):
                            scope_to_push = var_value.scope
                            self.environment.push_scope(var_value.scope)
                            n_scopes_release += 1
                        else:
                            raise RuntimeException(f"Getter of name {getter.identifier} doesn't resolve to an object")
                else:
                    if is_assign[0] and i == last_getter_idx:
                        new_var = Variable(name=getter.identifier, value=is_assign[1])
                        new_var.accept(self)
                    else:
                        raise RuntimeException(f"No variable of name {getter.identifier}")

            elif isinstance(getter, CallGetter):
                getter.accept(self, scope_to_push)
                result = self.environment.get_returned()
                if i != last_getter_idx:
                    if isinstance(result[1], Instance):
                        scope_to_push = result[1].scope
                        n_scopes_release += 1
                    else:
                        raise RuntimeException(message=f"Value behind variable {getter} is not an object")
                else:
                    if result[0]:
                        to_return = result[1]

                self.environment.reset_returned()

        return to_return

    def visit_identifier_getter(self, id_getter: IdentifierGetter):
        var = self.environment.get_variable(name=id_getter.get_identifier())
        return var

    def visit_call_getter(self, call_getter: CallGetter, scope_to_push=None):
        identifier = call_getter.get_identifier()


        if function_var := self.environment.get_variable(identifier):
            call_obj = function_var.value
            # TODO: Class constructor as a function (in class visiting)
            if call_obj:
                evaluated_args = call_getter.arguments.accept(self)
                if isinstance(call_obj, Function):
                    if scope_to_push:
                        self.environment.push_new_call_context(scope_to_push)
                        self.environment.push_scope()
                    else:
                        self.environment.push_new_call_context()

                    call_obj.params.accept(self)
                    self.set_parameter_values([call_obj] + evaluated_args, [call_obj.identifier] + call_obj.get_param_names())

                    call_obj.accept(self)
                    self.environment.pop_call_context()

                elif isinstance(call_obj, Class):
                    call_obj.accept(self, evaluated_args)

                elif isinstance(call_obj, NativeFunction):
                    call_obj.accept(self, evaluated_args)
        else:
            raise RuntimeException(f"Not found a function named {identifier}")

    def visit_arguments(self, arguments: Arguments):
        return [arg.accept(self) for arg in arguments.arguments]

    def visit_and_oper(self):
        # No need to visit this
        pass

    def visit_or_oper(self):
        # No need to visit this
        pass

    def visit_negative_oper(self, neg_operator, value=None):

        if isinstance(value, IntLiteral):
            internal_value = (-1) * value.value
            result = IntLiteral(value=internal_value)
        elif isinstance(value, FloatLiteral):
            internal_value = (-1) * value.value
            result = FloatLiteral(value=internal_value)
        else:
            raise RuntimeException("Cannot apply negative operator to object other than int or float")

        return result


    def visit_variable(self, variable: Variable):
        self.environment.add_variable(variable)

    def visit_comment(self, comment: Comment):
        pass
