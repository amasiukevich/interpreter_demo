from abc import ABC, abstractmethod

# from src.utils.program3.block import Block
# from src.utils.program3.classes._class import Class
# from src.utils.program3.classes.class_block import ClassBlock
# from src.utils.program3.expressions.math.add_expression import AddExpression
# from src.utils.program3.expressions.math.and_expression import AndExpression
# from src.utils.program3.expressions.math.equality_expression import EqualityExpression
# from src.utils.program3.expressions.math.multiply_expression import MultiplyExpression
# from src.utils.program3.expressions.math.or_expression import OrExpression
# from src.utils.program3.expressions.math.relation_expression import RelationExpression
# from src.utils.program3.expressions.math.unary_expression import UnaryExpression
# from src.utils.program3.expressions.operators.and_oper import AndOperator
# from src.utils.program3.expressions.operators.data_access_oper import DataAccessOperator
# from src.utils.program3.expressions.operators.divide_oper import DivideOperator
# from src.utils.program3.expressions.operators.equal_oper import EqualityOperator
# from src.utils.program3.expressions.operators.greater_equal_oper import GreaterEqualOperator
# from src.utils.program3.expressions.operators.greater_oper import GreaterOperator
# from src.utils.program3.expressions.operators.less_equal_oper import LessEqualOperator
# from src.utils.program3.expressions.operators.less_oper import LessOperator
# from src.utils.program3.expressions.operators.minus_oper import MinusOperator
# from src.utils.program3.expressions.operators.modulo_oper import ModuloOperator
# from src.utils.program3.expressions.operators.multiply_oper import MultiplyOperator
# from src.utils.program3.expressions.operators.negative_oper import NegativeOperator
# from src.utils.program3.expressions.operators.not_equal_oper import NotEqualOperator
# from src.utils.program3.expressions.operators.not_oper import NotOperator
# from src.utils.program3.expressions.operators.or_operator import OrOperator
# from src.utils.program3.expressions.operators.plus_oper import PlusOperator
# from src.utils.program3.functions.arguments import Arguments
# from src.utils.program3.functions.function import Function
# from src.utils.program3.functions.parameters import Parameters
# from src.utils.program3.program import Program
# from src.utils.program3.statements._return import Return
# from src.utils.program3.statements.assign import Assign
# from src.utils.program3.statements.comment import Comment
# from src.utils.program3.statements.conditional import Conditional
# from src.utils.program3.statements.foreach_loop import ForeachLoop
# from src.utils.program3.statements.func_call import FunctionCall
# from src.utils.program3.statements.rest_function_call import RestFunctionCall
# from src.utils.program3.statements.statement import Statement
# from src.utils.program3.statements.while_loop import WhileLoop
# from src.utils.program3.values.complex_getter import ComplexGetter
# from src.utils.program3.values.iterative_getter import IterativeGetter
# from src.utils.program3.values.literals.bool_literal import BoolLiteral
# from src.utils.program3.values.literals.float_literal import FloatLiteral
# from src.utils.program3.values.literals.int_literal import IntLiteral
# from src.utils.program3.values.literals.string_literal import StringLiteral
# from src.utils.program3.values.value import Value
# from src.utils.program3.variable import Variable


class Visitor(ABC):

    @abstractmethod
    def visit_program(self, program):
        pass

    @abstractmethod
    def visit_function(self, function):
        pass

    @abstractmethod
    def visit_class(self, _class):
        pass

    @abstractmethod
    def visit_parameters(self, parameters):
        pass

    @abstractmethod
    def visit_block(self, block):
        pass

    @abstractmethod
    def visit_class_block(self, class_block):
        pass

    @abstractmethod
    def visit_statement(self, statement):
        pass

    @abstractmethod
    def visit_assign(self, assign):
        pass

    @abstractmethod
    def visit_comment(self, comment):
        pass

    @abstractmethod
    def visit_conditional(self, conditional):
        pass

    @abstractmethod
    def visit_foreach_loop(self, foreach_loop):
        pass

    @abstractmethod
    def visit_return(self, _return):
        pass

    @abstractmethod
    def visit_while_loop(self, while_loop):
        pass

    @abstractmethod
    def visit_function_call(self, function_call):
        pass

    @abstractmethod
    def visit_rest_function_call(self, rest_function_call):
        pass

    @abstractmethod
    def visit_arguments(self, arguments):
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

    ### VALUES

    @abstractmethod
    def visit_complex_getter(self, complex_getter):
        pass

    @abstractmethod
    def visit_iterative_getter(self, iterative_getter):
        pass

    @staticmethod
    def visit_literal(self):
        pass

    ### OPERATORS

    # @abstractmethod
    # def visit_and_oper(self, and_oper):
    #     pass
    #
    # @abstractmethod
    # def visit_data_access_oper(self, data_access_oper):
    #     pass
    #
    # @abstractmethod
    # def visit_divide_oper(self, divide_oper):
    #     pass
    #
    # @abstractmethod
    # def visit_equal_oper(self, eq_oper):
    #     pass
    #
    # @abstractmethod
    # def visit_greater_equal_oper(self, ge_oper):
    #     pass
    #
    # @abstractmethod
    # def visit_greater_oper(self, gt_oper):
    #     pass
    #
    # @abstractmethod
    # def visit_less_equal_oper(self, le_oper):
    #     pass
    #
    # @abstractmethod
    # def visit_less_oper(self, lt_oper):
    #     pass
    #
    # @abstractmethod
    # def visit_minus_oper(self, minus_oper):
    #     pass
    #
    # @abstractmethod
    # def visit_modulo_oper(self, modulo_oper):
    #     pass
    #
    # @abstractmethod
    # def visit_multiply_oper(self, mult_oper):
    #     pass
    #
    # @abstractmethod
    # def visit_negative_oper(self, neg_oper):
    #     pass
    #
    # @abstractmethod
    # def visit_not_equal_oper(self, not_eq_oper):
    #     pass
    #
    # @abstractmethod
    # def visit_not_oper(self, not_oper):
    #     pass
    #
    # @abstractmethod
    # def visit_or_oper(self, or_oper):
    #     pass
    #
    # @abstractmethod
    # def visit_plus_oper(self, plus_operator):
    #     pass
