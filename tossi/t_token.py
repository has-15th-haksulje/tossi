# t_token.py

from enum import Enum


class TokenType(Enum):
    EOF = "EOF"
    IDENTIFIER = "IDENTIFIER"
    INTEGER = "INTEGER"
    STRING = "STRING"
    INDENT = "INDENT"
    DEDENT = "DEDENT"
    LPAREN = "LPAREN"  # (
    RPAREN = "RPAREN"  # )
    LBRACE = "LBRACE"  # {
    RBRACE = "RBRACE"  # }
    LSQB = "LSQB"  # [
    RSQB = "RSQB"  # ]
    COLON = "COLON"  # :
    SEMI = "SEMI"  # ;
    COMMA = "COMMA"  # ,
    PLUS = "PLUS"  # +
    MINUS = "MINUS"  # -
    STAR = "STAR"  # *
    SLASH = "SLASH"  # /
    VBAR = "VBAR"  # |
    AMPER = "AMPER"  # &
    LESS = "LESS"  # <
    GREATER = "GREATER"  # >
    PERCENT = "PERCENT"  # %
    DBLEQUAL = "DBLEQUAL"  # ==
    NOTEQUAL = "NOTEQUAL"  # !=
    LESSEQUAL = "LESSEQUAL"  # <=
    GREATEREQUAL = "GREATEREQUAL"  # >=
    TILDE = "TILDE"  # ~
    CARET = "CARET"  # ^
    DBLSTAR = "DBLSTAR"  # **
    DBLSLASH = "DBLSLASH"  # //
    AT = "AT"  # @
    ELLIPSIS = "ELLIPSIS"  # ...
    EXCLAM = "EXCLAM"  # !
    DOT = "DOT"  # .
    PARTICLE_SBJ = "PARTICLE_SBJ"  # 주격 조사 (이, 가)
    PARTICLE_OBJ = "PARTICLE_OBJ"  # 목적격 조사 (을, 를)
    PARTICLE_ADV = "PARTICLE_ADV"  # 부사격 조사 (에)
    PARTICLE_AUX = "PARTICLE_AUX"  # 보조사 (은, 는)
    IF = "IF"  # 참이라면
    ELSE = "ELSE"  # 아니라면
    WHILE = "WHILE"  # 동안
    PRINT = "PRINT"  # 보인다
    ASSIGN = "ASSIGN"  # 담는다
    RETURN = "RETURN"  # 돌려준다
    PARAMETER = "PARAMETER"  # 매개변수
    CALL = "CALL"  # 부른다
    COMMENT = "COMMENT"  # 주석

    BINOP = "BINOP"  # 이항 연산자
    COMPARE = "COMPARE"  # 비교 연산자


class Token:
    def __init__(self, type: TokenType, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"

    def __str__(self):
        return self.__repr__()
