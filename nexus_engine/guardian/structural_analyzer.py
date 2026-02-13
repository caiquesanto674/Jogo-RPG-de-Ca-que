"""
Módulo do Analisador Estrutural do Nexus Guardian.
"""

import ast
import hashlib
from typing import Dict

class StructuralAnalyzer:
    """Analisador estrutural com tratamento de erros"""

    def map_file(self, code: str, name: str) -> Dict:
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return {
                "functions": [],
                "classes": [],
                "imports": [],
                "hash": hashlib.sha256(code.encode()).hexdigest(),
                "erro_sintaxe": str(e),
                "valido": False
            }

        structure = {
            "functions": [],
            "classes": [],
            "imports": [],
            "hash": hashlib.sha256(code.encode()).hexdigest(),
            "valido": True
        }

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                structure["functions"].append({
                    "nome": node.name,
                    "args": len(node.args.args),
                    "linha": node.lineno
                })
            elif isinstance(node, ast.ClassDef):
                structure["classes"].append({
                    "nome": node.name,
                    "linha": node.lineno,
                    "metodos": [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                })
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                # Em Python 3.9+, podemos usar ast.unparse
                # Para compatibilidade, vamos manter uma representação simples
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        structure["imports"].append(f"import {alias.name}")
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ''
                    for alias in node.names:
                        structure["imports"].append(f"from {module} import {alias.name}")

        return structure
