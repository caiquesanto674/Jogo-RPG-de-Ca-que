from typing import Dict


class Tecnologia:
    """Gerenciamento do progresso tecnológico através de uma árvore de tecnologias."""

    def __init__(self):
        self.arvore: Dict[str, int] = {
            "IA": 1,
            "Fusao": 0,
            "Plasma": 1,
            "Biotecnologia": 0,
        }
        self.pesquisas_concluidas = []

    def pesquisar(self, tema: str):
        """Aumenta o nível de uma tecnologia na árvore."""
        if tema in self.arvore:
            self.arvore[tema] += 1
            self.pesquisas_concluidas.append(tema)
        else:
            # Se a tecnologia não existe, podemos adicioná-la ou registrar um erro.
            # Por agora, vamos apenas adicioná-la com nível 1.
            self.arvore[tema] = 1
            self.pesquisas_concluidas.append(tema)

    def __str__(self):
        return f"Tecnologia (Níveis: {self.arvore})"
