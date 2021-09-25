from .keyword_mapper import KeywordMapper
from src.data_sources.base_source import BaseSource
from src.exceptions.scanning_exception import ScanningException
from src.utils.token import Token
from src.utils.token_type import TokenType
from src.utils.position import Position

class Scanner:

    def __init__(self, source: BaseSource):

        self.source = source
        self.kw_mapper = KeywordMapper()
        self.token = Token(TokenType.UNKNOWN, Position(1, 0))

        # for keywords and identifiers
        self.tmp_keyword_id = ""
        self.tmp_kw_len = 0

    def get_token_and_move(self):
        temp_token = self.token
        self.next_token()
        return temp_token

    def get_token(self):
        return self.token

    def next_token(self):

        self.ignore_whitespaces()
        self.token_position = self.source.get_position().clone()
        if self.construct_eof():
            return
        elif self.construct_single_char_oper():
            return
        elif self.construct_double_char_oper():
            return
        elif self.construct_number():
            return
        elif self.construct_number():
            return
        elif self.construct_string_literal():
            return
        elif self.construct_identifier():
            return
        elif self.construct_comment():
            return
        elif self.construct_keyword():
            return
        else:
            self.token = Token(TokenType.UNKNOWN, position=self.token_position)
            raise ScanningException(self.token_position, "Unknown symbol")

    def ignore_whitespaces(self):

        while self.source.get_char() != -1 and self.source.get_char().isspace():
            self.source.read_char()

    def construct_eof(self):

        not_existing_character = (self.source.get_char() == -1)

        if not_existing_character:
            self.token = Token(token_type=TokenType.EOF, position=self.token_position)

        return not_existing_character


    def construct_single_char_oper(self):

        """
        Recognizes single char operators
        that doesn't have double-char equivalents
        """
        tmp_token_type = self.kw_mapper.SINGLE_CHAR_MAP.get(self.source.get_char())
        if tmp_token_type:
            self.token = Token(tmp_token_type, position=self.token_position, value=self.source.get_char())
            self.source.read_char()

        return bool(tmp_token_type)

    def construct_double_char_oper(self):

        is_recognized = True
        if self.source.get_char() == ">":
            # TODO: Can I refactor this ???
            self.source.read_char()
            second_char = self.source.get_char()
            if second_char == "=":
                self.token = Token(TokenType.GREATER_EQUAL, position=self.token_position, value=">=")
                self.source.read_char()
            else:
                self.token = Token(TokenType.GREATER, position=self.token_position, value=">")

        elif self.source.get_char() == "<":
            # TODO: Can I refactor this ???
            self.source.read_char()
            second_char = self.source.get_char()
            if second_char == "=":
                self.token = Token(TokenType.LESS_EQUAL, position=self.token_position, value="<")
                self.source.read_char()
            else:
                self.token = Token(TokenType.LESS, position=self.token_position, value="<=")

        elif self.source.get_char() == "!":
            # TODO: Can I refactor this ???
            self.source.read_char()
            second_char = self.source.get_char()
            if second_char == "=":
                self.token = Token(TokenType.NOT_EQUAL, position=self.token_position, value="!=")
                self.source.read_char()
            else:
                self.token = Token(TokenType.NOT, position=self.token_position, value="!")

        elif self.source.get_char() == "=":
            # TODO: Can I refactor this ???
            self.source.read_char()
            second_char = self.source.get_char()
            if second_char == "=":
                self.token = Token(TokenType.EQUAL, position=self.token_position, value="==")
                self.source.read_char()
            else:
                self.token = Token(TokenType.ASSIGN, position=self.token_position, value="=")

        elif self.source.get_char() == "&":
            # TODO: Can I refactor this ???
            self.source.read_char()
            second_char = self.source.get_char()
            if second_char == "&":
                self.token = Token(TokenType.AND, position=self.token_position, value="&&")
                self.source.read_char()
            else:
                is_recognized = False

        elif self.source.get_char() == "|":
            # TODO: Can I refactor this ???
            self.source.read_char()
            second_char = self.source.get_char()
            if second_char == "|":
                self.token = Token(TokenType.OR, position=self.token_position, value="||")
                self.source.read_char()
            else:
                is_recognized = False
        else:
            is_recognized = False

        return is_recognized

    def construct_number(self):
        pass

    def construct_string_literal(self):
        pass

    def construct_identifier(self):
        pass

    def construct_comment(self):
        pass

    def construct_keyword(self):
        pass