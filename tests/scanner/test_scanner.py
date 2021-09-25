from src.data_sources.string_source import StringSource
from src.data_sources.file_source import FileSource
from src.scanner.scanner import Scanner
from src.utils.token import Token
from src.utils.token_type import TokenType
from src.utils.position import Position


import io
import unittest


class TestScanner(unittest.TestCase):


    def test_construct_eof(self):

        source = StringSource(
            io.StringIO("")
        )

        scanner = Scanner(source)
        scanner.get_token_and_move()
        token = scanner.get_token()

        self.assertEqual(
            token, Token(TokenType.EOF, Position(1, 0))
        )


    def test_construct_single_char_tokens(self):

        source = StringSource(
            io.StringIO("{}[]()%/*-+;,.")
        )

        # TODO: refactor this part into separate method for testing purposes
        scanner = Scanner(source)
        scanner.get_token_and_move()
        token = scanner.get_token_and_move()

        tokens = []
        while token.token_type != TokenType.EOF:
            tokens.append(token)
            token = scanner.get_token_and_move()


        self.assertListEqual(
            tokens, [
                Token(TokenType.OPEN_CURLY_BRACKET, Position(1, 1)),
                Token(TokenType.CLOSING_CURLY_BRACKET, Position(1, 2)),
                Token(TokenType.OPEN_BRACKET, Position(1, 3)),
                Token(TokenType.CLOSING_BRACKET, Position(1, 4)),
                Token(TokenType.OPEN_PARENTHESIS, Position(1, 5)),
                Token(TokenType.CLOSING_PARENTHESIS, Position(1, 6)),
                Token(TokenType.MODULO, Position(1, 7)),
                Token(TokenType.DIVIDE, Position(1, 8)),
                Token(TokenType.MULTIPLY, Position(1, 9)),
                Token(TokenType.MINUS, Position(1, 10)),
                Token(TokenType.PLUS, Position(1, 11)),
                Token(TokenType.SEMICOLON, Position(1, 12)),
                Token(TokenType.COMMA, Position(1, 13)),
                Token(TokenType.ACCESS, Position(1, 14)),
            ]
        )

    def test_construct_double_char_tokens(self):

        source = StringSource(
            io.StringIO("&& || < >= > <= != == = !")
        )

        # TODO: refactor this part into separate method for testing purposes
        scanner = Scanner(source)
        scanner.get_token_and_move()
        token = scanner.get_token_and_move()

        tokens = []
        while token.token_type != TokenType.EOF:
            tokens.append(token)
            token = scanner.get_token_and_move()

        self.assertListEqual(
            tokens, [
                Token(TokenType.AND, Position(1, 1)),
                Token(TokenType.OR, Position(1, 4)),
                Token(TokenType.LESS, Position(1, 7)),
                Token(TokenType.GREATER_EQUAL, Position(1, 9)),
                Token(TokenType.GREATER, Position(1, 12)),
                Token(TokenType.LESS_EQUAL, Position(1, 14)),
                Token(TokenType.NOT_EQUAL, Position(1, 17)),
                Token(TokenType.EQUAL, Position(1, 20)),
                Token(TokenType.ASSIGN, Position(1, 23)),
                Token(TokenType.NOT, Position(1, 25))
            ]
        )



    def test_construct_number(self):
        pass

    def test_construct_string_literal(self):
        pass

    def test_construct_identifier(self):
        pass

    def test_construct_keyword(self):
        pass

    def test_construct_comment(self):
        pass

    def base_test_function(self, file_obj: io.StringIO):
        pass