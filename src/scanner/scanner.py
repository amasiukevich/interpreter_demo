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
        """
        Recognizes EOF token
        """
        not_existing_character = (self.source.get_char() == -1)

        if not_existing_character:
            self.token = Token(token_type=TokenType.EOF, position=self.token_position, value=None)

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

        """
        Recognizes double-char tokens as well as some single-char tokens
        :return:    is_recognized - bool
        """
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
                self.token = Token(TokenType.LESS_EQUAL, position=self.token_position, value="<=")
                self.source.read_char()
            else:
                self.token = Token(TokenType.LESS, position=self.token_position, value="<")

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

        if not self.source.get_char().isdigit():
            return False

        int_part = self.construct_integer_part()

        frac_part = 0
        if self.source.get_char() == ".":
            self.source.read_char()
            frac_part = self.construct_fractional_part()

        self.token = Token(TokenType.NUMERIC_LITERAL, position=self.token_position, value=(int_part + frac_part))
        return True


    def construct_integer_part(self):

        if self.is_zero_integer():
            return 0

        return self.construct_non_zero_integer()


    def is_zero_integer(self):

        is_zero = False

        if self.source.get_char() == "0":
            self.source.read_char()
            if self.source.get_char().isdigit():
                raise ScanningException(position=self.token_position,
                                        message="An integer part of number cannot start with 0")
            else:
                is_zero = True

        return is_zero


    def construct_non_zero_integer(self):

        int_value = 0
        while self.is_numerically_valid(self.source.get_char()) and int_value < Token.MAX_NUMBER:
            int_value = int_value * 10 + (ord(self.source.get_char()) - ord('0'))
            self.source.read_char()

        if int_value > Token.MAX_NUMBER:
            raise ScanningException(position=self.token_position,
                                    message="Exceeded maximum number limit")
        return int_value

    @staticmethod
    def is_numerically_valid(char):

        if isinstance(char, int):
            return char != -1
        elif isinstance(char, str):
            return char.isdigit()

    def construct_fractional_part(self):

        frac_value = 0
        exponent = self.ignore_zeros() + 1

        while self.is_numerically_valid(self.source.get_char()):
            frac_value += (ord(self.source.get_char()) - ord("0")) * 10 ** (-exponent)
            exponent += 1
            self.source.read_char()

        return frac_value


    def ignore_zeros(self):

        num_ignored = 0
        while self.source.get_char() == "0":
            num_ignored += 1
            self.source.read_char()

        return num_ignored


    def construct_string_literal(self):

        if self.source.get_char() != "\"":
            return False

        str_literal_value = ""
        self.source.read_char()
        while self.source.get_char() != "\"":

            if self.source.get_char() in ["\n", -1]:
                raise ScanningException(position=self.token_position,
                                        message="Missing closing \"")

            str_literal_value += self.source.get_char()
            self.source.read_char()

        self.token = Token(TokenType.STRING_LITERAL, position=self.token_position, value=str_literal_value)
        self.source.read_char()

        return True

    # TODO: refactor it for single responsibility of constructing identifier and a keyword
    def construct_identifier(self):

        self.tmp_keyword_id = ""
        self.tmp_kw_len = 0

        if self.is_begin_valid():

            while self.is_valid_part() and self.tmp_kw_len < Token.MAX_IDENTIFIER_LENGTH:

                self.tmp_keyword_id += self.source.get_char()
                self.tmp_kw_len += 1
                self.source.read_char()

            if self.is_valid_part():
                raise ScanningException(position=self.token_position,
                                        message="Length of the identifier exceeded")

            if self.construct_keyword():
                return True

            self.token = Token(TokenType.IDENTIFIER, position=self.token_position, value=self.tmp_keyword_id)
            return True

        else:
            return False


    def is_begin_valid(self):

        # for keywords and identifiers
        if self.source.get_char().isalpha():

            self.tmp_keyword_id += self.source.get_char()
            self.tmp_kw_len += 1
            self.source.read_char()

            return True
        # for identifiers only
        elif self.source.get_char() in ["$", "_"]:

            self.tmp_keyword_id += self.source.get_char()
            self.source.read_char()

            if self.is_valid_part():

                self.tmp_keyword_id += self.source.get_char()
                self.tmp_kw_len += 2
                self.source.read_char()

                return True
            else:
                raise ScanningException(position=self.token_position,
                                        message="Invalid identifier")

        else:
            return False


    def is_valid_part(self):
        return isinstance(self.source.get_char(), str) and \
               (self.source.get_char().isalnum() or self.source.get_char() == "_")


    def construct_keyword(self):

        tmp_keyword_name = self.kw_mapper.KEYWORD_MAP.get(self.tmp_keyword_id)
        if tmp_keyword_name:
            self.token = Token(token_type=tmp_keyword_name, position=self.token_position, value=self.tmp_keyword_id)

        return bool(tmp_keyword_name)

    def construct_comment(self):

        is_recognized = self.source.get_char() == "#"
        if is_recognized:

            comment_body = ""
            self.source.read_char()
            while self.source.get_char() not in ["\n", -1]:
                comment_body += self.source.get_char()
                self.source.read_char()
            self.token = Token(TokenType.COMMENT, position=self.token_position, value=comment_body)

        return is_recognized