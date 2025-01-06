# runtime.py

from parser import Parser

from interpreter import Interpreter
from lexer import Lexer


class Runtime:
    def __init__(self):
        self.lexer = Lexer()
        self.parser = Parser()
        self.interpreter = Interpreter()

    def run(self, source_code: str):
        self.interpreter.execute(  # AST 실행
            self.parser.generate(  # AST 생성
                self.lexer.tokenize(  # 토큰 생성
                    source_code
                )
            )
        )

    def repl(self):
        while True:
            source_code = input("토씨> ")

            if source_code == "exit":
                break

            elif source_code == "env":
                print(self.interpreter.env)

            self.run(source_code)


if __name__ == "__main__":
    import sys

    runtime = Runtime()

    if sys.argv[1:]:
        with open(sys.argv[1], encoding="UTF-8") as f:
            source_code = f.read()

            runtime.run(source_code)

    else:
        runtime.repl()
