from src.data_sources.string_source import StringSource
from src.scanner.scanner import Scanner
from src.utils.token import Token
from src.utils.token_type import TokenType
from src.utils.position import Position
from src.exceptions.scanning_exception import ScanningException


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
            token, Token(TokenType.EOF, Position(1, 0), value=None)
        )


    def test_construct_single_char_tokens(self):

        string_io = io.StringIO("{}[]()%/*-+;,.")
        tokens = self.base_test_function(string_io)

        self.assertListEqual(
            tokens, [
                Token(TokenType.OPEN_CURLY_BRACKET, Position(1, 1), value="{"),
                Token(TokenType.CLOSING_CURLY_BRACKET, Position(1, 2), value="}"),
                Token(TokenType.OPEN_BRACKET, Position(1, 3), value="["),
                Token(TokenType.CLOSING_BRACKET, Position(1, 4), value="]"),
                Token(TokenType.OPEN_PARENTHESIS, Position(1, 5), value="("),
                Token(TokenType.CLOSING_PARENTHESIS, Position(1, 6), value=")"),
                Token(TokenType.MODULO, Position(1, 7), value="%"),
                Token(TokenType.DIVIDE, Position(1, 8), value="/"),
                Token(TokenType.MULTIPLY, Position(1, 9), value="*"),
                Token(TokenType.MINUS, Position(1, 10), value="-"),
                Token(TokenType.PLUS, Position(1, 11), value="+"),
                Token(TokenType.SEMICOLON, Position(1, 12), value=";"),
                Token(TokenType.COMMA, Position(1, 13), value=","),
                Token(TokenType.ACCESS, Position(1, 14), value="."),
            ]
        )

    def test_construct_double_char_tokens(self):

        string_io = io.StringIO("&& || < >= > <= != == = !")
        tokens = self.base_test_function(string_io)

        self.assertListEqual(
            tokens, [
                Token(TokenType.AND, Position(1, 1), value="&&"),
                Token(TokenType.OR, Position(1, 4), value="||"),
                Token(TokenType.LESS, Position(1, 7), value="<"),
                Token(TokenType.GREATER_EQUAL, Position(1, 9), value=">="),
                Token(TokenType.GREATER, Position(1, 12), value=">"),
                Token(TokenType.LESS_EQUAL, Position(1, 14), "<="),
                Token(TokenType.NOT_EQUAL, Position(1, 17), value="!="),
                Token(TokenType.EQUAL, Position(1, 20), value="=="),
                Token(TokenType.ASSIGN, Position(1, 23), value="="),
                Token(TokenType.NOT, Position(1, 25), value="!")
            ]
        )

    def test_construct_number(self):

        string_io = io.StringIO("123; -123")
        tokens = self.base_test_function(string_io)

        self.assertListEqual(
            tokens, [
                Token(TokenType.NUMERIC_LITERAL, position=Position(1, 1), value=123),
                Token(TokenType.SEMICOLON, position=Position(1, 4), value=";"),
                Token(TokenType.MINUS, position=Position(1, 6), value="-"),
                Token(TokenType.NUMERIC_LITERAL, position=Position(1, 7), value=123)
            ]
        )


    def test_fractional_number(self):

        string_io = io.StringIO("7.405, 123.0001")
        tokens = self.base_test_function(string_io)

        self.assertListEqual(
            tokens, [
                Token(TokenType.NUMERIC_LITERAL, position=Position(1, 1), value=7.405),
                Token(TokenType.COMMA, position=Position(1, 6), value=","),
                Token(TokenType.NUMERIC_LITERAL, position=Position(1, 8), value=123.0001)
            ]
        )

    def test_leading_zero(self):

        string_io = io.StringIO("000123")
        exception_text =  f"ScanningException at position: {Position(1, 1)}\n" \
                          f"An integer part of number cannot start with 0"

        self.base_exception_test_function(string_io, exception_text)


    def test_max_number(self):

        string_io = io.StringIO("1200000000000000000000000000000000000000000000000000000;")
        exception_text = f"ScanningException at position: {Position(1, 1)}\n" \
                         f"Exceeded maximum number limit"

        self.base_exception_test_function(string_io, exception_text)


    def test_construct_identifier(self):

        string_io = io.StringIO("a = 10;")
        tokens = self.base_test_function(string_io)

        self.assertListEqual(
            tokens, [
                Token(TokenType.IDENTIFIER, position=Position(1, 1), value="a"),
                Token(TokenType.ASSIGN, position=Position(1, 3), value="="),
                Token(TokenType.NUMERIC_LITERAL, position=Position(1, 5), value=10),
                Token(TokenType.SEMICOLON, position=Position(1, 7), value=";")
            ]
        )

    def test_id_length(self):

        string_io = io.StringIO("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                                "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                                "aaaaaaaa")

        exception_text = f"ScanningException at position: {Position(1, 1)}\n" \
                         f"Length of the identifier exceeded"

        self.base_exception_test_function(string_io, exception_text)


    def test_construct_string_literal(self):

        string_io = io.StringIO("\"Anton\"")
        tokens = self.base_test_function(string_io)

        self.assertListEqual(
            tokens, [
                Token(TokenType.STRING_LITERAL, position=Position(1, 1), value="Anton")
            ]
        )


    def test_not_closed_string(self):

        string_io = io.StringIO("\"Ala ma kota")
        exception_text = f"ScanningException at position: {Position(1, 1)}\n" \
                         f"Missing closing \""

        self.base_exception_test_function(string_io, exception_text)


    def test_construct_keyword(self):

        string_io = io.StringIO("define class this if else foreach while in return reflect recursive by_ref true false")
        tokens = self.base_test_function(string_io)

        self.assertListEqual(
            tokens, [
                Token(TokenType.DEFINE, position=Position(1, 1), value="define"),
                Token(TokenType.CLASS, position=Position(1, 8), value="class"),
                Token(TokenType.THIS, position=Position(1, 14), value="this"),
                Token(TokenType.IF, position=Position(1, 19), value="if"),
                Token(TokenType.ELSE, position=Position(1, 22), value="else"),
                Token(TokenType.FOREACH, position=Position(1, 27), value="foreach"),
                Token(TokenType.WHILE, position=Position(1, 35), value="while"),
                Token(TokenType.IN, position=Position(1, 41), value="in"),
                Token(TokenType.RETURN, position=Position(1, 44), value="return"),
                Token(TokenType.REFLECT, position=Position(1, 51), value="reflect"),
                Token(TokenType.RECURSIVE, position=Position(1, 59), value="recursive"),
                Token(TokenType.BY_REF, position=Position(1, 69), value="by_ref"),
                Token(TokenType.BOOL_LITERAL, position=Position(1, 76), value="true"),
                Token(TokenType.BOOL_LITERAL, position=Position(1, 81), value="false")
            ]
        )

    def test_invalid_identifier(self):

        string_io = io.StringIO("$'")

        exception_text = f"ScanningException at position: {Position(1, 1)}\n" \
                         f"Invalid identifier"
        pass


    def test_construct_comment(self):

        string_io = io.StringIO(
            "# this is a comment\n#And 123 this is also a comment\n"
            "# And foreach and any purpose I can define this a comment while sitting next door"
        )

        tokens = self.base_test_function(string_io)

        self.assertListEqual(
            tokens, [
                Token(TokenType.COMMENT, position=Position(1, 1), value=" this is a comment"),
                Token(TokenType.COMMENT, position=Position(2, 1), value="And 123 this is also a comment"),
                Token(TokenType.COMMENT, position=Position(3, 1),
                      value=" And foreach and any purpose I can define this a comment while sitting next door")
            ]
        )

    def base_test_function(self, string_file_obj: io.StringIO):

        source = StringSource(string_file_obj)

        scanner = Scanner(source)
        scanner.get_token_and_move()
        token = scanner.get_token_and_move()

        tokens = []
        while token.token_type != TokenType.EOF:
            tokens.append(token)
            token = scanner.get_token_and_move()

        return tokens

    def base_exception_test_function(self, string_file_obj: io.StringIO, exception_text: str):

        source = StringSource(string_file_obj)

        scanner = Scanner(source)

        with self.assertRaises(ScanningException) as context:
            scanner.next_token()

        the_exception = context.exception

        self.assertEqual(
            the_exception.get_message(),
            exception_text
        )



