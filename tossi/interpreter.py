# interpreter.py

import ast

from exception import InterpreterException


class Interpreter:
    def __init__(self):
        self.env = {}

    def exception(self, message: str):
        raise InterpreterException(message)

    def execute(self, tree: ast.Module):
        code = compile(tree, "<interpreter>", "exec")

        exec(code, None, self.env)
