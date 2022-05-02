from abc import ABCMeta, abstractmethod


class Visitor(metaclass=ABCMeta):

    @abstractmethod
    def visit_program(self, program):
        pass

    @abstractmethod
    def visit_function(self, function):
        pass

    @abstractmethod
    def visit_class(self, _class, constructor_params):
        pass

    @abstractmethod
    def visit_parameters(self, parameters):
        pass

    @abstractmethod
    def visit_block(self, block):
        pass

    @abstractmethod
    def visit_class_block(self, class_block, instance):
        pass

    @abstractmethod
    def visit_function_call(self, function_call):
        pass

    @abstractmethod
    def visit_native_function(self, native_function, evaluated_args):
        pass

    @abstractmethod
    def visit_or_expression(self, or_expression):
        pass

    @abstractmethod
    def visit_and_expression(self, and_expression):
        pass

    @abstractmethod
    def visit_eq_expression(self, eq_expression):
        pass

    @abstractmethod
    def visit_rel_expression(self, rel_expression):
        pass

    @abstractmethod
    def visit_add_expression(self, add_expression):
        pass

    @abstractmethod
    def visit_mult_expression(self, mult_expression):
        pass

    @abstractmethod
    def visit_unary_expression(self, unary_expression):
        pass

    @abstractmethod
    def visit_equal_oper(self, equal_oper):
        pass

    @abstractmethod
    def visit_not_equal_oper(self, not_eq_oper, value):
        pass

    @abstractmethod
    def visit_not_oper(self, not_oper, value):
        pass

    @abstractmethod
    def visit_greater_equal_oper(self, ge_oper, left_value, right_value):
        pass

    @abstractmethod
    def visit_greater_oper(self, gt_oper, left_value, right_value):
        pass

    @abstractmethod
    def visit_less_equal_oper(self, le_oper, left_value, right_value):
        pass

    @abstractmethod
    def visit_less_oper(self, lt_oper, left_value, right_value):
        pass

    @abstractmethod
    def visit_plus_oper(self, plus_operator, left_value, right_value):
        pass

    @abstractmethod
    def visit_minus_oper(self, minus_operator, left_value, right_value):
        pass

    @abstractmethod
    def visit_multiply_oper(self, mult_operator, left_value, right_value):
        pass

    @abstractmethod
    def visit_divide_oper(self, div_operator, left_value, right_value):
        pass

    @abstractmethod
    def visit_modulo_oper(self, modulo_operator, left_value, right_value):
        pass

    @abstractmethod
    def visit_or_oper(self, or_oper):
        pass

    @abstractmethod
    def visit_and_oper(self, and_oper):
        pass

    @abstractmethod
    def visit_negative_oper(self, neg_oper, value=None):
        pass

    @abstractmethod
    def visit_literal(self, literal):
        pass

    @abstractmethod
    def visit_complex_getter(self, complex_getter, is_assign):
        pass

    @abstractmethod
    def visit_arguments(self, arguments):
        pass

    @abstractmethod
    def visit_identifier_getter(self, identifier_getter):
        pass

    @abstractmethod
    def visit_call_getter(self, call_getter, scope_to_push):
        pass

    @abstractmethod
    def visit_variable(self, variable):
        pass
