# exception.py


class LexerException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class ParserException(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class InterpreterException(Exception):
    def __init__(self, message: str):
        super().__init__(message)
