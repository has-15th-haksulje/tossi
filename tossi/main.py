import ast

code = """
i = 0

while i < 3:
    print(i)
    i = i + 1
"""
node = ast.parse(code)

exec(compile(node, "<main>", "exec"))
print(ast.dump(node, indent=4))
