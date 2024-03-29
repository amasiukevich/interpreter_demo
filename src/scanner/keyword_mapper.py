from src.utils import TokenType


class KeywordMapper:

    KEYWORD_MAP = {
        "class" : TokenType.CLASS,
        "this" : TokenType.THIS,
        "if" : TokenType.IF,
        "else" : TokenType.ELSE,
        "foreach" : TokenType.FOREACH,
        "while": TokenType.WHILE,
        "in" : TokenType.IN,
        "return" : TokenType.RETURN,
        "true" : TokenType.BOOL_LITERAL,
        "false" : TokenType.BOOL_LITERAL,
        "null": TokenType.NULL_LITERAL
    }

    SINGLE_CHAR_MAP = {
        "." : TokenType.ACCESS,
        "," : TokenType.COMMA,
        ";" : TokenType.SEMICOLON,
        "+" : TokenType.PLUS,
        "-" : TokenType.MINUS,
        "*" : TokenType.MULTIPLY,
        "/" : TokenType.DIVIDE,
        "%" : TokenType.MODULO,
        "(" : TokenType.OPEN_PARENTHESIS,
        ")" : TokenType.CLOSING_PARENTHESIS,
        "[" : TokenType.OPEN_BRACKET,
        "]" : TokenType.CLOSING_BRACKET,
        "{" : TokenType.OPEN_CURLY_BRACKET,
        "}" : TokenType.CLOSING_CURLY_BRACKET
    }