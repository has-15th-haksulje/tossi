# lexer.py

from exception import LexerException
from t_token import Token, TokenType


class Lexer:
    def exception(self, message: str):
        raise LexerException(message)

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else ""

    def skip_whitespace(self):
        while self.current_char.isspace():
            self.advance()

    # 자료형 ---------------------------------------------------------------------------
    def integer(self):
        result = ""

        while self.current_char.isdigit():
            result += self.current_char

            self.advance()

        return int(result)

    def string(self):
        result = ""
        self.advance()  # Skip the opening quote

        while self.current_char != '"':
            result += self.current_char
            self.advance()

            if not self.current_char:
                self.exception("Unterminated string")

        self.advance()  # Skip the closing quote

        return result  # ---------------------------------------------------------------

    # 식별자 ---------------------------------------------------------------------------
    def identifier(self):
        result = ""

        while (
            self.current_char.isalnum()
            or self.current_char == "_"
            or ("가" <= self.current_char <= "힣")
        ):
            result += self.current_char
            self.advance()

        if result[-1] in ("이", "가", "을", "를", "에", "은", "는"):
            self.pos -= 1
            self.current_char = self.text[self.pos]

            result = result[:-1]

        return result  # ---------------------------------------------------------------

    # 어휘 분석 ------------------------------------------------------------------------
    def get_next_token(self):
        while self.current_char:
            if self.current_char.isspace():
                self.skip_whitespace()

            elif self.current_char == "(":
                self.advance()
                self.tokens.append(Token(TokenType.LPAREN, "("))

            elif self.current_char == ")":
                self.advance()
                self.tokens.append(Token(TokenType.RPAREN, ")"))

            elif self.current_char == ".":
                self.advance()
                self.tokens.append(Token(TokenType.DOT, "."))

            elif self.current_char == "+":
                self.advance()
                self.tokens.append(Token(TokenType.PLUS, "+"))

            elif self.current_char == "-":
                self.advance()
                self.tokens.append(Token(TokenType.MINUS, "-"))

            elif self.current_char == "*":
                self.advance()
                self.tokens.append(Token(TokenType.STAR, "*"))

            elif self.current_char == "/":
                self.advance()
                self.tokens.append(Token(TokenType.SLASH, "/"))

            elif self.current_char == "%":
                self.advance()
                self.tokens.append(Token(TokenType.PERCENT, "%"))

            elif self.text.startswith("==", self.pos):
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.DBLEQUAL, "=="))

            elif self.text.startswith("!=", self.pos):
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.NOTEQUAL, "!="))

            elif self.text.startswith("<=", self.pos):
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.LESSEQUAL, "<="))

            elif self.text.startswith(">=", self.pos):
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.GREATEREQUAL, ">="))

            elif self.current_char == "<":
                self.advance()
                self.tokens.append(Token(TokenType.LESS, "<"))

            elif self.current_char == ">":
                self.advance()
                self.tokens.append(Token(TokenType.GREATER, ">"))

            elif self.current_char in ("이", "가"):
                self.advance()
                self.tokens.append(Token(TokenType.PARTICLE_SBJ, "이"))

            elif self.current_char in ("을", "를"):
                self.advance()
                self.tokens.append(Token(TokenType.PARTICLE_OBJ, "을"))

            elif self.current_char == "에":
                self.advance()
                self.tokens.append(Token(TokenType.PARTICLE_ADV, "에"))

            elif self.current_char in ("은", "는"):
                self.advance()
                self.tokens.append(Token(TokenType.PARTICLE_AUX, "은"))

            elif self.text.startswith("참이라면", self.pos):
                self.advance()
                self.advance()
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.IF, "참이라면"))

            elif self.text.startswith("아니라면", self.pos):
                self.advance()
                self.advance()
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.ELSE, "아니라면"))

            elif self.text.startswith("담는다", self.pos):
                self.advance()
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.ASSIGN, "담는다"))

            elif self.text.startswith(("담자", "담음"), self.pos):
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.ASSIGN, "담는다"))

            elif self.text.startswith(
                ("보인다", "보이며", "보이고", "보이자"), self.pos
            ):
                self.advance()
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.PRINT, "보인다"))

            elif self.text.startswith("보임", self.pos):
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.PRINT, "보인다"))

            elif self.text.startswith(("돌려준다", "돌려주고"), self.pos):
                self.advance()
                self.advance()
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.RETURN, "돌려준다"))

            elif self.text.startswith("부른다", self.pos):
                self.advance()
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.CALL, "부른다"))

            elif self.text.startswith("참인 동안", self.pos):
                self.advance()
                self.advance()
                self.advance()
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.WHILE, "참인 동안"))

            elif self.current_char.isdigit():
                integer = self.integer()
                self.tokens.append(Token(TokenType.INTEGER, integer))

            elif self.current_char == '"':
                string = self.string()
                self.tokens.append(Token(TokenType.STRING, string))

            elif (
                self.current_char.isalpha()
                or self.current_char == "_"
                or ("가" <= self.current_char <= "힣")
            ):
                identifier = self.identifier()
                self.tokens.append(Token(TokenType.IDENTIFIER, identifier))

            else:
                self.exception("Invalid character")

        self.tokens.append(Token(TokenType.EOF, ""))

    def tokenize(self, text: str):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else ""
        self.tokens: list[Token] = []
        self.paren_count = 0

        while self.current_char:
            self.get_next_token()

        return self.tokens  # ----------------------------------------------------------
