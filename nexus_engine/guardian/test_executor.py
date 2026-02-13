"""
Módulo do Executor de Testes do Nexus Guardian.
"""

import re
from datetime import datetime
from typing import Dict

class TestExecutor:
    """
    Executor de testes básicos para verificação de sanidade do código.
    """

    def run_basic_tests(self, code: str) -> Dict:
        """
        Executa uma série de testes básicos, como verificação de sintaxe
        e presença de estruturas essenciais.
        """
        result = {
            "timestamp": datetime.now().isoformat(),
            "sintaxe_valida": True,
            "erros": [],
            "metricas": {
                "linhas": 0,
                "classes": 0,
                "funcoes": 0,
                "imports": 0
            }
        }

        # 1. Teste de Sintaxe
        try:
            compile(code, "<string>", "exec")
        except SyntaxError as e:
            result["sintaxe_valida"] = False
            result["erros"].append(f"Erro de Sintaxe: {e.msg} na linha {e.lineno}")
        except Exception as e:
            result["sintaxe_valida"] = False
            result["erros"].append(f"Erro de Compilação: {str(e)}")

        # 2. Extração de Métricas Básicas
        lines = code.splitlines()
        result["metricas"]["linhas"] = len(lines)

        # Usando regex para uma contagem simples e robusta
        result["metricas"]["classes"] = len(re.findall(r'^\s*class\s+\w+', code, re.MULTILINE))
        result["metricas"]["funcoes"] = len(re.findall(r'^\s*def\s+\w+', code, re.MULTILINE))
        result["metricas"]["imports"] = len(re.findall(r'^\s*import\s+|^\s*from\s+', code, re.MULTILINE))

        # 3. Verificação de "Más Práticas" (heurística simples)
        if "eval(" in code:
            result["erros"].append("Uso perigoso de 'eval()' detectado.")
        if "exec(" in code:
            result["erros"].append("Uso perigoso de 'exec()' detectado.")

        return result
