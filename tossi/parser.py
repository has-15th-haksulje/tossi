# parser.py

import ast

from exception import ParserException
from t_token import Token, TokenType


class Parser:
    def exception(self, message: str):
        raise ParserException(message)

    def op_to_ast(self, token: Token):
        if token.type == TokenType.PLUS:
            return ast.Add()

        elif token.type == TokenType.MINUS:
            return ast.Sub()

        elif token.type == TokenType.STAR:
            return ast.Mult()

        elif token.type == TokenType.SLASH:
            return ast.Div()

        elif token.type == TokenType.PERCENT:
            return ast.Mod()

    def compare_to_ast(self, token: Token):
        if token.type == TokenType.LESS:
            return ast.Lt()

        elif token.type == TokenType.GREATER:
            return ast.Gt()

        elif token.type == TokenType.DBLEQUAL:
            return ast.Eq()

        elif token.type == TokenType.NOTEQUAL:
            return ast.NotEq()

        elif token.type == TokenType.LESSEQUAL:
            return ast.LtE()

        elif token.type == TokenType.GREATEREQUAL:
            return ast.GtE()

    def ast_bin_op(self, left: Token, op: Token, right: Token):
        tree = ast.BinOp(
            left=(
                (
                    ast.Name(id=left.value, ctx=ast.Load(), lineno=1, col_offset=0)
                    if left.type == TokenType.IDENTIFIER
                    else ast.Constant(value=left.value, lineno=1, col_offset=0)
                )
                if left.type != TokenType.BINOP
                else self.ast_bin_op(*left.value)
            ),
            op=self.op_to_ast(op),
            right=(
                (
                    ast.Name(id=right.value, ctx=ast.Load(), lineno=1, col_offset=0)
                    if right.type == TokenType.IDENTIFIER
                    else ast.Constant(value=right.value, lineno=1, col_offset=0)
                )
                if right.type != TokenType.BINOP
                else self.ast_bin_op(*right.value)
            ),
            lineno=1,
            col_offset=0,
        )

        return tree

    def ast_compare(self, left: Token, op: Token, right: Token):
        if left.type == TokenType.IDENTIFIER:
            left = ast.Name(id=left.value, ctx=ast.Load(), lineno=1, col_offset=0)

        elif left.type == TokenType.BINOP:
            left = self.ast_bin_op(*left.value)

        else:
            left = ast.Constant(value=left.value, lineno=1, col_offset=0)

        if right.type == TokenType.IDENTIFIER:
            right = ast.Name(id=right.value, ctx=ast.Load(), lineno=1, col_offset=0)

        elif right.type == TokenType.BINOP:
            right = self.ast_bin_op(*right.value)

        else:
            right = ast.Constant(value=right.value, lineno=1, col_offset=0)

        tree = ast.Compare(
            left=left,
            ops=[self.compare_to_ast(op)],
            comparators=[right],
            lineno=1,
            col_offset=0,
        )

        return tree

    def ast_if(self, tokens: list[Token]):
        for token in tokens:
            if token.type == TokenType.PARTICLE_SBJ:
                previous_token = tokens[tokens.index(token) - 1]

                if previous_token.type == TokenType.IDENTIFIER:
                    test = ast.Name(
                        id=previous_token.value, ctx=ast.Load(), lineno=1, col_offset=0
                    )

                elif previous_token.type == TokenType.BINOP:
                    test = self.ast_bin_op(*previous_token.value)

                elif previous_token.type == TokenType.COMPARE:
                    test = self.ast_compare(*previous_token.value)

                else:
                    test = ast.Constant(
                        value=previous_token.value, lineno=1, col_offset=0
                    )

            elif token.type == TokenType.IF:
                body_tokens = tokens[tokens.index(token) + 1 :]

                if TokenType.ELSE in map(lambda x: x.type, body_tokens):
                    else_index = body_tokens.index(
                        next(filter(lambda x: x.type == TokenType.ELSE, body_tokens))
                    )
                    body = self.generate(
                        body_tokens[:else_index] + [Token(TokenType.DOT, ".")]
                    ).body
                    orelse = self.generate(body_tokens[else_index + 1 :]).body

                else:
                    body = self.generate(body_tokens).body
                    orelse = []

        if_node = ast.If(
            test=test,
            body=body,
            orelse=orelse,
            lineno=1,
            col_offset=0,
        )

        return if_node

    def ast_while(self, tokens: list[Token]):
        body_tokens = []

        for token in tokens:
            if token.type == TokenType.PARTICLE_SBJ:
                previous_token = tokens[tokens.index(token) - 1]

                if previous_token.type == TokenType.COMPARE:
                    test = self.ast_compare(*previous_token.value)

            elif token.type == TokenType.WHILE:
                for body_token in tokens[tokens.index(token) + 1 :]:
                    body_tokens.append(body_token)

                    if body_token.type in (
                        TokenType.ASSIGN,
                        TokenType.PRINT,
                        TokenType.CALL,
                    ):
                        body_tokens.append(Token(TokenType.DOT, "."))

                body_tokens.pop()

        body = self.generate(body_tokens).body

        while_node = ast.While(
            test=test,
            body=body,
            lineno=1,
            col_offset=0,
        )

        return while_node

    def ast_assign(self, tokens: list[Token]):
        is_identifier = False

        for token in tokens:
            if token.type.name.startswith("PARTICLE"):
                previous_token = tokens[tokens.index(token) - 1]

                if token.type == TokenType.PARTICLE_ADV:
                    identifier = previous_token.value

                elif token.type == TokenType.PARTICLE_OBJ:
                    value = previous_token.value

                    if previous_token.type == TokenType.IDENTIFIER:
                        is_identifier = True

                    elif previous_token.type == TokenType.BINOP:
                        value = self.ast_bin_op(*previous_token.value)

        assign_node = ast.Assign(
            targets=[ast.Name(id=identifier, ctx=ast.Store(), lineno=1, col_offset=0)],
            value=(
                value
                if isinstance(value, ast.BinOp)
                else (
                    ast.Name(id=value, ctx=ast.Load(), lineno=1, col_offset=0)
                    if is_identifier
                    else ast.Constant(value=value, lineno=1, col_offset=0)
                )
            ),
            lineno=1,
            col_offset=0,
        )

        return assign_node

    def ast_print(self, tokens: list[Token]):
        args = []

        for token in tokens:
            if (
                token.type == TokenType.IDENTIFIER
                and tokens[tokens.index(token) + 1].type == TokenType.LPAREN
            ):
                start = tokens.index(token)
                function_args = []

                while tokens[start].type != TokenType.RPAREN:
                    function_args.append(tokens[start])
                    start += 1

                function_args.append(Token(TokenType.RPAREN, ")"))
                args.append(self.ast_call(function_args).value)

            if token.type == TokenType.PARTICLE_OBJ:
                previous_token = tokens[tokens.index(token) - 1]

                if previous_token.type == TokenType.RPAREN:
                    continue

                if previous_token.type == TokenType.IDENTIFIER:
                    args.append(
                        ast.Name(
                            id=previous_token.value,
                            ctx=ast.Load(),
                            lineno=1,
                            col_offset=0,
                        )
                    )

                elif previous_token.type == TokenType.BINOP:
                    args.append(self.ast_bin_op(*previous_token.value))

                else:
                    args.append(
                        ast.Constant(value=previous_token.value, lineno=1, col_offset=0)
                    )

        print_node = ast.Expr(
            value=ast.Call(
                func=ast.Name(id="print", ctx=ast.Load(), lineno=1, col_offset=0),
                args=args,
                lineno=1,
                col_offset=0,
            ),
            lineno=1,
            col_offset=0,
        )

        return print_node

    def ast_return(self, tokens: list[Token]):
        for token in tokens:
            if (
                token.type == TokenType.IDENTIFIER
                and tokens[tokens.index(token) + 1].type == TokenType.LPAREN
            ):
                start = tokens.index(token)
                function_args = []

                while tokens[start].type != TokenType.RPAREN:
                    function_args.append(tokens[start])
                    start += 1

                function_args.append(Token(TokenType.RPAREN, ")"))
                value = self.ast_call(function_args).value

            if token.type == TokenType.PARTICLE_OBJ:
                previous_token = tokens[tokens.index(token) - 1]

                if previous_token.type == TokenType.IDENTIFIER:
                    value = ast.Name(
                        id=previous_token.value,
                        ctx=ast.Load(),
                        lineno=1,
                        col_offset=0,
                    )

                elif previous_token.type == TokenType.BINOP:
                    value = self.ast_bin_op(*previous_token.value)

                else:
                    value = ast.Constant(
                        value=previous_token.value, lineno=1, col_offset=0
                    )

        return_node = ast.Return(
            value=value,
            lineno=1,
            col_offset=0,
        )

        return return_node

    def ast_function_def(self, tokens: list[Token]):
        body_tokens: list[Token] = []

        for token in tokens[
            tokens.index(
                next(filter(lambda x: x.type == TokenType.PARTICLE_AUX, tokens))
            )
            + 1 :
        ]:
            body_tokens.append(token)

            if token.type in (
                TokenType.ASSIGN,
                TokenType.PRINT,
                TokenType.RETURN,
                TokenType.CALL,
            ):
                body_tokens.append(Token(TokenType.DOT, "."))

        body_tokens.pop()
        body = self.generate(body_tokens).body
        # token_buffer: list[Token] = []

        # for body_token in body_tokens:
        #     token_buffer.append(body_token)

        #     if body_token.type == TokenType.DOT:
        #         for buffered_token in token_buffer:
        #             if buffered_token.type == TokenType.IF:
        #                 body.append(self.ast_if(token_buffer))

        #             elif buffered_token.type == TokenType.ASSIGN:
        #                 body.append(self.ast_assign(token_buffer))

        #             elif buffered_token.type == TokenType.PRINT:
        #                 body.append(self.ast_print(token_buffer))

        #             elif buffered_token.type == TokenType.RETURN:
        #                 body.append(self.ast_return(token_buffer))

        #             elif buffered_token.type == TokenType.CALL:
        #                 body.append(self.ast_call(token_buffer))

        #         token_buffer.clear()

        rparen_index = tokens.index(
            next(filter(lambda x: x.type == TokenType.RPAREN, tokens))
        )

        tree = ast.FunctionDef(
            name=tokens[0].value,
            args=ast.arguments(
                args=[
                    ast.arg(arg=token.value, annotation=None, lineno=1, col_offset=0)
                    for token in tokens[2:rparen_index]
                    if token.type == TokenType.IDENTIFIER
                ]
            ),
            body=body,
            lineno=1,
            col_offset=0,
        )

        return tree

    def ast_call(self, tokens: list[Token]):
        function_name = next(
            filter(lambda x: x.type == TokenType.IDENTIFIER, tokens[::-1])
        )
        start = tokens.index(function_name) + 2
        args = []

        while tokens[start].type != TokenType.RPAREN:
            token = tokens[start]

            if token.type == TokenType.IDENTIFIER:
                args.append(
                    ast.Name(id=token.value, ctx=ast.Load(), lineno=1, col_offset=0)
                )

            elif token.type == TokenType.BINOP:
                args.append(self.ast_bin_op(*token.value))

            else:
                args.append(ast.Constant(value=token.value, lineno=1, col_offset=0))

            start += 1

        call_node = ast.Expr(
            value=ast.Call(
                func=ast.Name(
                    id=function_name.value, ctx=ast.Load(), lineno=1, col_offset=0
                ),
                args=args,
                lineno=1,
                col_offset=0,
            ),
            lineno=1,
            col_offset=0,
        )

        return call_node

    def generate(self, tokens: list[Token]):
        token_buffer: list[Token] = []
        asts = []

        # 이항 연산자 처리
        for op in list(
            filter(
                lambda x: x.type
                in (TokenType.STAR, TokenType.SLASH, TokenType.PERCENT),
                tokens,
            )
        ):
            left = tokens.pop(tokens.index(op) - 1)
            right = tokens.pop(tokens.index(op) + 1)

            tokens[tokens.index(op)] = Token(TokenType.BINOP, [left, op, right])

        for op in list(
            filter(lambda x: x.type in (TokenType.PLUS, TokenType.MINUS), tokens)
        ):
            if tokens[tokens.index(op) - 1].type == TokenType.RPAREN:
                continue

            left = tokens.pop(tokens.index(op) - 1)
            right = tokens.pop(tokens.index(op) + 1)

            tokens[tokens.index(op)] = Token(TokenType.BINOP, [left, op, right])

        # 비교 연산자 처리
        for op in list(
            filter(
                lambda x: x.type
                in (
                    TokenType.LESS,
                    TokenType.GREATER,
                    TokenType.DBLEQUAL,
                    TokenType.NOTEQUAL,
                    TokenType.LESSEQUAL,
                    TokenType.GREATEREQUAL,
                ),
                tokens,
            )
        ):
            left = tokens.pop(tokens.index(op) - 1)
            right = tokens.pop(tokens.index(op) + 1)

            tokens[tokens.index(op)] = Token(TokenType.COMPARE, [left, op, right])

        for token in tokens:
            token_buffer.append(token)

            if token.type == TokenType.DOT:
                if TokenType.PARTICLE_AUX in map(lambda x: x.type, token_buffer):
                    asts.append(self.ast_function_def(token_buffer))
                    token_buffer.clear()

                elif TokenType.PARTICLE_SBJ in map(lambda x: x.type, token_buffer):
                    if TokenType.IF in map(lambda x: x.type, token_buffer):
                        asts.append(self.ast_if(token_buffer))
                        token_buffer.clear()

                    elif TokenType.WHILE in map(lambda x: x.type, token_buffer):
                        asts.append(self.ast_while(token_buffer))
                        token_buffer.clear()

                for buffered_token in token_buffer:
                    if buffered_token.type == TokenType.ASSIGN:
                        asts.append(self.ast_assign(token_buffer))

                    elif buffered_token.type == TokenType.PRINT:
                        asts.append(self.ast_print(token_buffer))

                    elif buffered_token.type == TokenType.RETURN:
                        asts.append(self.ast_return(token_buffer))

                    elif buffered_token.type == TokenType.CALL:
                        asts.append(self.ast_call(token_buffer))

                token_buffer.clear()

        return ast.Module(asts)
