import ast

try:
    with open("nexus_engine.py", "r") as f:
        code = f.read()
    ast.parse(code)
    print("Sintaxe OK")
except SyntaxError as e:
    print(f"Erro de sintaxe encontrado: {e}")
    print(f"Linha: {e.lineno}")
    print(f"Coluna: {e.offset}")
    print(f"Texto: {e.text}")
