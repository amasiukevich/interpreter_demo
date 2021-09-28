from src.utils.program3.expressions.operators.operator import Operator
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

from src.utils.token_type import TokenType
from src.utils.token import Token

from typing import Union


class OperatorMapper:

    def __init__(self):
        self.token_to_operator = self.init_token_to_oper_map()
        self.token_to_operator_additive = self.init_token_to_oper_additive_map()

    @staticmethod
    def init_token_to_oper_map() -> dict:

        token_type_to_operator = {
            TokenType.AND: AndOperator(),
            TokenType.ACCESS: DataAccessOperator(),
            TokenType.DIVIDE: DivideOperator(),
            TokenType.EQUAL: EqualityOperator(),
            TokenType.GREATER_EQUAL: GreaterEqualOperator(),
            TokenType.GREATER: GreaterOperator(),
            TokenType.LESS_EQUAL: LessEqualOperator(),
            TokenType.LESS: LessOperator(),
            TokenType.MINUS: NegativeOperator(),
            TokenType.MODULO: ModuloOperator(),
            TokenType.MULTIPLY: MultiplyOperator(),
            TokenType.NOT_EQUAL: NotEqualOperator(),
            TokenType.NOT: NotOperator(),
            TokenType.OR: OrOperator()
        }

        return token_type_to_operator

    @staticmethod
    def init_token_to_oper_additive_map() -> dict:

        token_type_to_operator_additive = {
            TokenType.MINUS: MinusOperator(),
            TokenType.PLUS: PlusOperator()
        }

        return token_type_to_operator_additive

    def construct_operator(self, token: Token) -> Union[Operator, None]:

        operator = self.token_to_operator.get(token.get_token_type())
        return operator

    def construct_additive_operator(self, token: Token) -> Union[Operator, None]:

        operator = self.token_to_operator_additive.get(token.get_token_type())
        return operator
