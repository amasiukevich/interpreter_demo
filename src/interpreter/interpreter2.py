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
from ..utils.program3.functions.parameters import Parameters
from ..utils.program3.statements._return import Return
from ..utils.program3.statements.assign import Assign
from ..utils.program3.statements.conditional import Conditional
from ..utils.program3.statements.func_call import FunctionCall
from ..utils.program3.statements.while_loop import WhileLoop
from ..utils.program3.values.complex_getter import ComplexGetter
from ..utils.program3.values.iterative_getter import CallGetter, IdentifierGetter
from ..utils.program3.values.literals.bool_literal import BoolLiteral
from ..utils.program3.values.literals.float_literal import FloatLiteral
from ..utils.program3.values.literals.int_literal import IntLiteral
from ..utils.program3.values.literals.literal import Literal
from ..utils.program3.values.literals.string_literal import StringLiteral
from ..utils.program3.values.value import Value
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
        self.global_environment = Environment()
        self.environment = self.global_environment

        self.move_program_objects()

    def execute(self):
        self.program.accept(self)

    # def init_native_functions(self):
    #
    #     # print
    #     native_print = NativeFunction(arity=1, call_func=print)
    #     self.program.function_dict['print'] = native_print

    def move_program_objects(self):

        for func_name, func_obj in self.program.function_dict.items():
            self.global_environment.add_variable(Variable(name=func_name, value=func_obj))

        for cls_name, cls_obj in self.program.class_dict.items():
            self.global_environment.add_variable(Variable(name=cls_name, value=cls_obj))

        # native print
        native_print = NativeFunction(arity=1, call_func=print)
        self.global_environment.add_variable(Variable(name='print', value=native_print))

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
        function.get_params().accept(self)
        # set parameter values here (binding)

        self.set_parameter_values(function.get_params())

        function.get_block().accept(self)

    def visit_class(self, _class: Class):

        # TODO: Create the constructor recognizable
        constructor_params = []
        for i in range(len(_class.get_constructor().get_params()) - 1):
            constructor_params.append(self.environment.pop_value())

        constructor_params = constructor_params[::-1]

        instance = Instance(klass=_class)
        self.environment = instance.environment

        for param in constructor_params:
            self.environment.push_value(param)

        self.environment.push_value(instance)

        _class.class_block.accept(self)

    def visit_parameters(self, parameters: Parameters):

        # TODO: Inside the function's call context create variables of the same name as parameters
        param_names = parameters.get_param_names()
        for name in param_names:
            variable = Variable(name=name, value=None)
            self.environment.add_variable(variable)

    def set_parameter_values(self, parameters: Parameters):

        param_names = parameters.get_param_names()

        for param_name in param_names:
            # TODO: maybe some casting here???
            variable = self.environment.get_variable(param_name)
            variable.value = self.environment.pop_value()

    def visit_block(self, block: Block):

        self.environment.push_new_scope()
        for statement in block.get_statements():
            statement.accept(self)
        self.environment.pop_scope()

    def visit_class_block(self, class_block: ClassBlock):

        instance = self.environment.pop_value()
        constructor = instance.klass.get_constructor()

        # add call context for class properties
        self.environment.push_new_call_context()

        # register this
        instance.environment.add_variable(Variable(name='this', value=instance))

        # TODO: Add here attributes
        # TODO: Add here rec_attributes

        for method in instance.klass.get_methods():
            if method != constructor:
                function = Variable(method.identifier, value=method)
                instance.environment.add_variable(function)

        # TODO: Push values that go with the constructor to the stack
        # evaluate constructor
        constructor.accept(self)
        self.environment.push_value(instance)

    def visit_function_call(self, function_call: FunctionCall):

        # TODO: Adapt to the new code!!!

        # TODO: what if until last getter - it gets resolved by the complex getter, but last one - from other

        env_current, env_to_return = function_call.getter.accept(self)

        self.environment = env_current
        last_getter = function_call.getter.get_last_getter()
        if not isinstance(last_getter, CallGetter):
            # TODO: write better exception
            raise RuntimeException(f"Expected a function call")

        identifier = last_getter.get_identifier()
        if function_obj := self.environment.get_variable(identifier).value:

            # evaluate arguments
            for arg in function_call.get_arguments():
                arg.accept(self)

            # perform a call
            function_obj.accept(self)

            # transfering result to the right place
            result = self.environment.pop_value()
            self.environment = env_to_return
            self.environment.push_value(result)

        # Visit value getter before the run
        # complex_getter = function_call.getter
        # env = self.environment
        # last_getter_idx = len(complex_getter.iterative_getters) - 1
        # for i, getter in enumerate(complex_getter.iterative_getters):
        #     if isinstance(getter, IdentifierGetter):
        #         var = env.get_variable(getter.get_identifier())
        #         if var:
        #             if i == last_getter_idx:
        #
        #     pass

        identifier = function_call.get_callee_name()
        for arg in function_call.get_arguments():
            arg.accept(self)

        if function_obj := self.environment.get_variable(identifier).value:
            function_obj.accept(self)
        else:
            # TODO: custom exception here
            raise RuntimeException(f"Function of name {identifier} does not exist")

    def visit_native_function(self, native_function: NativeFunction):

        arguments = []
        for i in range(native_function.arity):
            arguments.append(self.environment.pop_value().value)

        native_function.call_func(*arguments)

    # Statements
    def visit_assign(self, assign: Assign):

        # TODO: Some things about returns/broken/continued etc...
        # TODO: Do some dangerous stuff to support objects etc...

        assign.expression.accept(self)
        right_value = self.environment.pop_value()

        # left part
        env = self.environment
        last_getter_idx = len(assign.complex_getter.iterative_getters) - 1
        for i, it_getter in enumerate(assign.complex_getter.iterative_getters):

            if isinstance(it_getter, IdentifierGetter):
                var = env.get_variable(it_getter.get_identifier())
                if var:
                    if i != last_getter_idx and isinstance(var.value, Instance):
                        env = var.value.environment
                    else:
                        var.set_value(right_value)
                else:
                    if i == last_getter_idx:
                        variable = Variable(name=it_getter.get_identifier(), value=right_value)
                        tmp_env, self.environment = self.environment, env
                        variable.accept(self)
                        self.environment = tmp_env
                    else:
                        # TODO: get there fancy message about not found attribute in object
                        raise RuntimeException(message=f"Object has no attribute {it_getter.get_identifier()}", token=None)
            elif isinstance(it_getter, CallGetter):
                call_complex_getter = ComplexGetter(has_this=assign.complex_getter.has_this)
                function_call_obj = FunctionCall(call_complex_getter)
                tmp_env, self.environment = self.environment, env
                function_call_obj.accept(self)

                result = self.environment.pop_value()
                self.environment = tmp_env
                if i != last_getter_idx:
                    if isinstance(result, Instance):
                        env = result.environment
                    else:
                        raise Exception("Function call doesn't evaluate to object")
                else:
                    raise Exception("Cannot assign to function call")

    def visit_return(self, _return: Return):

        if self.environment.is_returned():
            return

        if expression := _return.expression:
            expression.accept(self)
            self.environment.set_returned_with_value(True)

        self.environment.set_returned(True)

    def visit_while_loop(self, while_loop: WhileLoop):

        if self.environment.is_returned():
            return

        condition, body = while_loop.expression, while_loop.block
        condition.accept(self)
        # TODO: work on this!!!
        condition_value = self.environment.pop_value().value # TODO: Maybe casting here???

        while condition_value and not self.environment.is_returned():
            body.accept(self)
            condition.accept(self)
            condition_value = self.environment.pop_value().value

    def visit_conditional(self, conditional: Conditional):

        if self.environment.is_returned():
            return

        block_chosen = False
        for i, condition in enumerate(conditional.expressions):

            condition.accept(self)
            condition_value = self.environment.pop_value().value # TODO: Maybe some casting here

            if condition_value:
                conditional.blocks[i].accept(self)
                block_chosen = True
                break

        # else case
        if not block_chosen and not conditional.is_single_if():
            conditional.blocks[-1].accept(self)

    def visit_or_expression(self, or_expression: OrExpression):

        # # TODO: Get rid of those
        # if not isinstance(or_expression, OrExpression):
        #     self.visit_and_expression(or_expression)

        value = False
        for expression in or_expression.expressions:
            expression.accept(self)
            temp = self.environment.pop_value().value # TODO: maybe some casting here
            value = value or temp

        self.environment.push_value(BoolLiteral(value))

    def visit_and_expression(self, and_expression: AndExpression):

        # if not isinstance(and_expression, AndExpression):
        #     self.visit_eq_expression(and_expression)
        # pass

        value = True
        for expression in and_expression.expressions:
            expression.accept(self)
            temp = self.environment.pop_value().value # TODO: Maybe some casting here
            value = value and temp

        self.environment.push_value(BoolLiteral(value))

    def visit_eq_expression(self, eq_expression: EqualityExpression):

        # if not isinstance(eq_expression, EqualityExpression):
        #     self.visit_rel_expression(eq_expression)

        # evaluating expressions
        eq_expression.expressions[0].accept(self)
        eq_expression.expressions[1].accept(self)

        eq_expression.operator.accept(self)

    def visit_rel_expression(self, rel_expression: RelationExpression):

        # if not isinstance(rel_expression, RelationExpression):
        #     self.visit_add_expression(rel_expression)

        rel_expression.expressions[0].accept(self)
        rel_expression.expressions[1].accept(self)

        rel_expression.operator.accept(self)

    def visit_add_expression(self, add_expression: AddExpression):

        if not isinstance(add_expression, AddExpression):
            self.visit_mult_expression(add_expression)
        else:
            add_expression.expressions[0].accept(self)
            for i in range(1, add_expression.get_num_expressions()):
                add_expression.expressions[i].accept(self)
                current_oper = add_expression.operators[i - 1]
                current_oper.accept(self)

    def visit_mult_expression(self, mult_expression: MultiplyExpression):

        if not isinstance(mult_expression, MultiplyExpression):
            self.visit_unary_expression(mult_expression)
        else:
            mult_expression.expressions[0].accept(self)
            for i in range(1, mult_expression.get_num_expressions()):
                mult_expression.expressions[i].accept(self)
                current_oper = mult_expression.operators[i - 1]
                current_oper.accept(self)

    def visit_unary_expression(self, unary_expression: UnaryExpression):

        if isinstance(unary_expression, Literal):
            unary_expression.accept(self)
        elif isinstance(unary_expression, ComplexGetter):
            unary_expression.accept(self)
        else:
            pass

    # TODO: later refactor all of the methods
    def visit_equal_oper(self, eq_oper: EqualityOperator):

        right_value = self.environment.pop_value().value
        left_value = self.environment.pop_value().value

        self.environment.push_value(BoolLiteral(left_value == right_value))

    def visit_not_equal_oper(self, not_eq_oper: NotEqualOperator):

        right_value = self.environment.pop_value().value
        left_value = self.environment.pop_value().value

        self.environment.push_value(BoolLiteral(left_value != right_value))

    def visit_not_oper(self, not_oper: NotOperator):

        value = self.environment.pop_value().value
        # TODO: cast to boolean
        self.environment.push_value(BoolLiteral(not value))

    def visit_greater_oper(self, gt_oper: GreaterOperator):
        right_value = self.environment.pop_value().value
        left_value = self.environment.pop_value().value

        self.environment.push_value(BoolLiteral(left_value > right_value))

    def visit_greater_equal_oper(self, ge_oper: GreaterEqualOperator):
        right_value = self.environment.pop_value().value
        left_value = self.environment.pop_value().value

        self.environment.push_value(BoolLiteral(left_value >= right_value))

    def visit_less_oper(self, lt_oper: LessOperator):
        right_value = self.environment.pop_value().value
        left_value = self.environment.pop_value().value

        self.environment.push_value(BoolLiteral(left_value < right_value))

    def visit_less_equal_oper(self, le_oper: LessEqualOperator):
        right_value = self.environment.pop_value().value
        left_value = self.environment.pop_value().value

        self.environment.push_value(BoolLiteral(left_value <= right_value))

    def visit_plus_oper(self, plus_operator: PlusOperator):

        right_literal = self.environment.pop_value()
        left_literal = self.environment.pop_value()

        result = None
        if isinstance(left_literal, StringLiteral) and isinstance(right_literal, StringLiteral):
            result_val = left_literal.value + right_literal.value
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

        self.environment.push_value(result)

    def visit_minus_oper(self, minus_operator: MinusOperator):

        right_literal = self.environment.pop_value()
        left_literal = self.environment.pop_value()

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

        self.environment.push_value(result)

    def visit_multiply_oper(self, mult_operator: MultiplyOperator):

        right_literal = self.environment.pop_value()
        left_literal = self.environment.pop_value()

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

        self.environment.push_value(result)

    def visit_divide_oper(self, div_operator: DivideOperator):

        right_literal = self.environment.pop_value()
        left_literal = self.environment.pop_value()

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

        self.environment.push_value(result)

    def visit_modulo_oper(self, modulo_operator: ModuloOperator):

        right_literal = self.environment.pop_value()
        left_literal = self.environment.pop_value()

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

        self.environment.push_value(result)

    def visit_literal(self, literal: Literal):
        self.environment.push_value(literal)

    def visit_complex_getter(self, complex_getter: ComplexGetter):

        if complex_getter.get_last_identifier() == 'sayHello':
            print("Hey there")

        env = self.environment
        last_getter_idx = len(complex_getter.iterative_getters) - 1
        for i, getter in enumerate(complex_getter.iterative_getters):

            if isinstance(getter, IdentifierGetter):
                var = env.get_variable(getter.get_identifier())
                if var:
                    if i == last_getter_idx:
                        self.environment.push_value(var.value)
                    else:
                        if var and isinstance(var.value, Instance):
                            env = var.value.environment
                        else:
                            raise RuntimeException(message="Cannot access field or method of non-object variable", token=None)
                else:
                    raise RuntimeException(token=None, message=f"No variable or function of name {getter.identifier}")

            elif isinstance(getter, CallGetter):
                call_complex_getter = ComplexGetter(has_this=complex_getter.has_this, iterative_getters=complex_getter.iterative_getters[:i + 1])
                function_call_obj = FunctionCall(call_complex_getter)
                tmp_env, self.environment = self.environment, env
                function_call_obj.accept(self)

                result = self.environment.pop_value()
                self.environment = tmp_env

                if i != last_getter_idx:
                    if isinstance(result, Instance):
                        env = result.environment
                    else:
                        raise Exception("Can't access field or method of non-object variable")
                else:
                    # pushing it to the initial environment
                    self.environment.push_value(result)

    def visit_new_complex_getter(self, complex_getter: ComplexGetter):

        env_to_return, env = self.environment, self.environment
        for i in range(len(complex_getter.iterative_getters) - 1):
            getter = complex_getter.iterative_getters[i]
            if isinstance(getter, IdentifierGetter):
                var = env.get_variable(getter.get_identifier())

            elif isinstance(getter, CallGetter):
                pass

            pass


        return None
        pass


    def visit_and_oper(self):
        # No need to visit this
        pass

    def visit_or_oper(self):
        # No need to visit this
        pass

    def visit_variable(self, variable: Variable):
        self.environment.add_variable(variable)

    def visit_comment(self, comment: Comment):
        pass
