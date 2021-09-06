from enum import Enum, auto

class TokenType(Enum):

    # TOKENS
    IDENTIFIER = auto()                 # identifier
    COMMENT = auto()                    # comment

    # OPERATORS

    # ACCESS
    ASSIGN = auto()                     # =
    ACCESS = auto()                     # .

    # Logical

    OR = auto()                # ||
    AND = auto()                                 # &&
    NOT = auto()                        # !

    # Comparison operators
    EQUAL = auto()                      # ==
    NOT_EQUAL = auto()                  # !=

    GREATER = auto()                    # >
    GREATER_EQUAL = auto()              # >=
    LESS = auto()                       # <
    LESS_EQUAL = auto()                 # <=

    # Mathematical
    PLUS = auto()                       # +
    MINUS = auto()                      # -
    MULTIPLY = auto()                   # *
    DIVIDE = auto()                     # /
    MODULO = auto()                     # %

    # SYMBOLS
    OPEN_PARENTHESIS = auto()           # (
    CLOSING_PARENTHESIS = auto()        # )
    OPEN_BRACKET = auto()               # [
    CLOSING_BRACKE = auto()             # ]
    OPEN_CURLY_BRACKET = auto()         # {
    CLOSING_CURLY_BRACKET = auto()      # }
    SEMICOLON = auto()                  # ;
    COMMA = auto()                      # ,

    # Basic language instructions
    DEFINE = auto()                     # define
    CLASS = auto()                      # class
    THIS = auto()                       # this

    IF = auto()                         # if
    ELSE = auto()                       # else
    WHILE = auto()                      # while
    FOREACH = auto()                    # foreach
    IN = auto()                         # in

    RETURN = auto()                     # return

    REFLECT = auto()                    # reflect
    RECURSIVE = auto()                  # for 'reflect recursive'

    BY_REF = auto()

    BOOL_LITERAL = auto()               # true or false
    STRING_LITERAL = auto()             # "String"
    NUMERIC_LITERAL = auto()            # 123 or -123

    UNKNOWN = auto()
    EOF = auto()
