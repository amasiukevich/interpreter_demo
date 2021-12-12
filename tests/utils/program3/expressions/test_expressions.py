import unittest

from src.utils.program3.expressions.math.negative_unary_expression import NegativeUnaryExpression
from src.utils.program3.expressions.math.not_unary_expression import NotUnaryExpression

from src.exceptions.validation_exception import ValidationException
from src.utils.program3.expressions.expression import Expression
from src.utils.program3.expressions.math.add_expression import AddExpression
from src.utils.program3.expressions.math.and_expression import AndExpression
from src.utils.program3.expressions.math.equality_expression import EqualityExpression
from src.utils.program3.expressions.math.logical_expression import LogicalExpression
from src.utils.program3.expressions.math.multiply_expression import MultiplyExpression
from src.utils.program3.expressions.math.or_expression import OrExpression
from src.utils.program3.expressions.math.relation_expression import RelationExpression
from src.utils.program3.expressions.math.unary_expression import UnaryExpression
from src.utils.program3.expressions.operators.divide_oper import DivideOperator
from src.utils.program3.expressions.operators.equal_oper import EqualityOperator
from src.utils.program3.expressions.operators.greater_equal_oper import GreaterEqualOperator
from src.utils.program3.expressions.operators.less_oper import LessOperator
from src.utils.program3.expressions.operators.minus_oper import MinusOperator
from src.utils.program3.expressions.operators.modulo_oper import ModuloOperator
from src.utils.program3.expressions.operators.not_equal_oper import NotEqualOperator
from src.utils.program3.expressions.operators.or_operator import OrOperator
from src.utils.program3.expressions.operators.plus_oper import PlusOperator
from src.utils.program3.values.literals.bool_literal import BoolLiteral
from src.utils.program3.values.literals.int_literal import IntLiteral


class TestExpressions(unittest.TestCase):

    def test_add_expression_str(self):

        add_expression = AddExpression(
            [IntLiteral(1), IntLiteral(2)],
            [MinusOperator()]
        )

        string_obj = "(1 - 2)"
        self.assertEqual(str(add_expression), string_obj)

    def test_add_expression_repr(self):

        add_expression = AddExpression(
            [IntLiteral(1), IntLiteral(2)],
            [PlusOperator()]
        )

        repr_string = "AddExpression(operator=[+], 2)"
        self.assertEqual(add_expression.__repr__(), repr_string)

    def test_mult_expressions_str(self):

        mult_expression = MultiplyExpression(
            [IntLiteral(42), IntLiteral(4)],
            [DivideOperator()]
        )

        string_obj = "(42 / 4)"
        self.assertEqual(str(mult_expression), string_obj)

    def test_mult_expressions_repr(self):

        mult_expression = MultiplyExpression(
            [IntLiteral(42), IntLiteral(4)],
            [ModuloOperator()]
        )

        repr_string = "MultiplyExpression(operators=[%], 2)"
        self.assertEqual(mult_expression.__repr__(), repr_string)

    def test_eq_expression_str(self):

        eq_expression = EqualityExpression(
            [IntLiteral(2), IntLiteral(13)],
            [NotEqualOperator()]
        )

        string_obj = "(2 != 13)"
        self.assertEqual(str(eq_expression), string_obj)

    def test_eq_expression_repr(self):

        eq_expression = EqualityExpression(
            [IntLiteral(1), IntLiteral(5)],
            [EqualityOperator()]
        )

        repr_string = "EqualityExpression(operators=[==], 2)"
        self.assertEqual(eq_expression.__repr__(), repr_string)

    def test_rel_expression_str(self):

        rel_expression = RelationExpression(
            [IntLiteral(10), IntLiteral(123)],
            [LessOperator()]
        )

        string_obj = "(10 < 123)"
        self.assertEqual(str(rel_expression), string_obj)

    def test_rel_expression_repr(self):

        rel_expression = RelationExpression(
            [IntLiteral(10), IntLiteral(12)],
            [GreaterEqualOperator()]
        )

        repr_string = "RelationExpression(operators=[>=], 2)"
        self.assertEqual(rel_expression.__repr__(), repr_string)

    def test_arithmetic_expression_creation_fail(self):

        list_of_exception_strings = []
        list_to_compare = [
            "ValidationException: All expression components should be of Expression datatype",
            "ValidationException: All operator components should be of Operator datatype",
            "ValidationException: Number of exception components should be greater than number of operators by exactly 1"
        ]

        with self.assertRaises(ValidationException) as context:
            AddExpression([None, None], PlusOperator())

        the_exception = context.exception

        list_of_exception_strings.append(the_exception.get_message())

        with self.assertRaises(ValidationException) as context2:
            MultiplyExpression([IntLiteral(10), IntLiteral(12)], [None])

        the_exception = context2.exception
        list_of_exception_strings.append(the_exception.get_message())

        with self.assertRaises(ValidationException) as context3:
            EqualityExpression([IntLiteral(2), IntLiteral(3), IntLiteral(4)], [EqualityOperator()])

        the_exception = context3.exception
        list_of_exception_strings.append(the_exception.get_message())

        self.assertListEqual(
            list_of_exception_strings,
            list_to_compare
        )

    def test_and_expression_str(self):

        and_expression = AndExpression(
            [BoolLiteral(True), BoolLiteral(False)]
        )

        string_obj = "(True && False)"
        self.assertEqual(str(and_expression), string_obj)


    def test_and_expression_repr(self):

        and_expression = AndExpression(
            [BoolLiteral(True), BoolLiteral(False), BoolLiteral(True)]
        )

        repr_string = "AndExpression(n_expressions=3)"
        self.assertEqual(and_expression.__repr__(), repr_string)

    def test_or_expression_str(self):

        or_expression = OrExpression(
            [BoolLiteral(False), BoolLiteral(False)]
        )
        string_obj = "(False || False)"
        self.assertEqual(str(or_expression), string_obj)

    def test_or_expression_repr(self):

        or_expression = OrExpression(
            [BoolLiteral(True), BoolLiteral(False)]
        )

        repr_string = "OrExpression(n_expressions=2)"
        self.assertEqual(or_expression.__repr__(), repr_string)

    def test_logical_expression_creation_fail(self):

        list_of_exception_strings = []
        list_to_compare = [
            "ValidationException: All expression components should be of Expression datatype"
        ]
        with self.assertRaises(ValidationException) as context:
            LogicalExpression([None, None], OrOperator())

        the_exception = context.exception

        list_of_exception_strings.append(the_exception.get_message())

        self.assertListEqual(
            list_of_exception_strings,
            list_to_compare
        )

    def test_negative_unary_expression_str(self):

        negative_expression = NegativeUnaryExpression(
            IntLiteral(13)
        )

        string_obj = "-(13)"
        self.assertEqual(str(negative_expression), string_obj)

    def test_negative_unary_expression_repr(self):

        negative_expression = NegativeUnaryExpression(
            IntLiteral(2)
        )

        repr_string = "NegativeUnaryExpression()"
        self.assertEqual(negative_expression.__repr__(), repr_string)

    def test_not_unary_expression_str(self):

        not_expression = NotUnaryExpression(
            BoolLiteral(True)
        )

        string_obj = "!(True)"
        self.assertEqual(str(not_expression), string_obj)

    def test_not_unary_expression_repr(self):

        not_expression = NotUnaryExpression(
            BoolLiteral(True)
        )

        repr_string = "NotUnaryExpression()"
        self.assertEqual(not_expression.__repr__(), repr_string)

    def test_unary_expression_creation_fail(self):

        list_of_exception_strings = []
        list_to_compare = [
            "ValidationException: UnaryExpression object cannot be created without a proper expression",
            "ValidationException: UnaryExpression object cannot be created without a proper operator"
        ]
        with self.assertRaises(ValidationException) as context:
            UnaryExpression(None, NotEqualOperator())

        the_exception = context.exception

        list_of_exception_strings.append(the_exception.get_message())

        with self.assertRaises(ValidationException) as context2:
            UnaryExpression(Expression(), None)

        the_exception = context2.exception
        list_of_exception_strings.append(the_exception.get_message())

        self.assertListEqual(
            list_of_exception_strings,
            list_to_compare
        )
