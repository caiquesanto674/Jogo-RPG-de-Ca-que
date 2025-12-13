"""
Módulo do Analisador Semântico do Nexus Guardian.
"""

from typing import Dict, List, Set

class SemanticAnalyzer:
    """
    Analisa o 'significado' do código, extraindo conceitos e propósito.
    """

    def __init__(self):
        self.semantic_memory: Dict[str, Dict] = {}
        self.CONCEITOS_CHAVE: Set[str] = {
            "sistema", "engine", "militar", "mundo", "rpg",
            "economia", "ai", "combate", "inventario",
            "classe", "magia", "unificacao", "multiverso", "guardian",
            "log", "evento", "tempo", "energia", "entidade"
        }

    def analyze(self, code: str, file_name: str) -> Dict:
        """
        Extrai significado, propósito e domínios de cada arquivo.
        """
        code_lower = code.lower()

        detected = [kw for kw in self.CONCEITOS_CHAVE if kw in code_lower]

        # Heurística de complexidade baseada na densidade de palavras-chave
        # e estruturas de controle
        control_structures = code_lower.count("def ") + code_lower.count("class ") + \
                             code_lower.count("if ") + code_lower.count("for ") + \
                             code_lower.count("while ")

        complexity = (len(detected) * 2 + control_structures) // (len(code_lower.split()) // 100 + 1)

        summary = {
            "file": file_name,
            "concepts": sorted(list(set(detected))),
            "complexity": min(10, complexity) # Normaliza em uma escala de 0-10
        }

        self.semantic_memory[file_name] = summary
        return summary

    def compare_similarity(self, file_name1: str, file_name2: str) -> float:
        """
        Calcula a similaridade semântica entre dois arquivos analisados.
        Retorna um valor entre 0.0 e 1.0.
        """
        sem1 = self.semantic_memory.get(file_name1)
        sem2 = self.semantic_memory.get(file_name2)

        if not sem1 or not sem2:
            return 0.0

        concepts1 = set(sem1.get("concepts", []))
        concepts2 = set(sem2.get("concepts", []))

        if not concepts1 and not concepts2:
            return 1.0

        intersection = len(concepts1.intersection(concepts2))
        union = len(concepts1.union(concepts2))

        return intersection / union if union > 0 else 0.0
