from src.utils.program3.expressions.operators.oper_mapper import OperatorMapper

from src.utils.program3.expressions.operators.and_oper import AndOperator
from src.utils.program3.expressions.operators.data_access_oper import DataAccessOperator
from src.utils.program3.expressions.operators.divide_oper import DivideOperator
from src.utils.program3.expressions.operators.equal_oper import EqualityOperator
from src.utils.program3.expressions.operators.greater_equal_oper import GreaterEqualOperator
from src.utils.program3.expressions.operators.greater_oper import GreaterOperator
from src.utils.program3.expressions.operators.less_equal_oper import LessEqualOperator
from src.utils.program3.expressions.operators.less_oper import LessOperator
from src.utils.program3.expressions.operators.minus_oper import MinusOperator
from src.utils.program3.expressions.operators.modulo_oper import ModuloOperator
from src.utils.program3.expressions.operators.multiply_oper import MultiplyOperator
from src.utils.program3.expressions.operators.negative_oper import NegativeOperator
from src.utils.program3.expressions.operators.not_equal_oper import NotEqualOperator
from src.utils.program3.expressions.operators.not_oper import NotOperator
from src.utils.program3.expressions.operators.or_operator import OrOperator
from src.utils.program3.expressions.operators.plus_oper import PlusOperator

from src.utils.token import Token
from src.utils.token_type import TokenType
from src.utils.position import Position

from typing import List

import unittest

class TestOperMapper(unittest.TestCase):

    def test_operator_creation(self):

        tokens = [
            Token(TokenType.AND, Position(1, 1), value="&&"),
            Token(TokenType.ACCESS, Position(1, 3), value="."),
            Token(TokenType.DIVIDE, Position(1, 4), value="/"),
            Token(TokenType.EQUAL, Position(1, 5), value="=="),
            Token(TokenType.GREATER_EQUAL, Position(1, 7), value=">="),
            Token(TokenType.GREATER, Position(1, 9), value=">"),
            Token(TokenType.LESS_EQUAL, Position(1, 11), value="<="),
            Token(TokenType.LESS, Position(1, 13), value="<"),
            Token(TokenType.MINUS, Position(1, 14), value="-"),
            Token(TokenType.MODULO, Position(1, 15), value="%"),
            Token(TokenType.MULTIPLY, Position(1, 16), value="*"),
            Token(TokenType.NOT_EQUAL, Position(1, 17), value="!="),
            Token(TokenType.NOT, Position(1, 19), value="!"),
            Token(TokenType.OR, Position(1, 20), value="||")
        ]

        oper_mapper = OperatorMapper()
        operators = []

        for token in tokens:
            operators.append(oper_mapper.construct_operator(token))

        self.assertListEqual(
            operators, [
                AndOperator(),
                DataAccessOperator(),
                DivideOperator(),
                EqualityOperator(),
                GreaterEqualOperator(),
                GreaterOperator(),
                LessEqualOperator(),
                LessOperator(),
                NegativeOperator(),
                ModuloOperator(),
                MultiplyOperator(),
                NotEqualOperator(),
                NotOperator(),
                OrOperator()
            ]
        )

    def test_additive_operator_creation(self):

        tokens = [
            Token(TokenType.MINUS, Position(1, 1), value="-"),
            Token(TokenType.PLUS, Position(1, 2), value="+")
        ]

        oper_mapper = OperatorMapper()
        operators = []

        for token in tokens:
            operators.append(oper_mapper.construct_additive_operator(token))

        self.assertListEqual(
            operators, [
                MinusOperator(),
                PlusOperator()
            ]
        )