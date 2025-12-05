class Tecnologia:
    """Gerenciamento do progresso tecnológico."""
    def __init__(self): self.nivel, self.descobertas = 1, []
    def pesquisar(self, tema): self.nivel += 1; self.descobertas.append(tema)
    def __str__(self): return f"Tecnologia (Nível: {self.nivel})"
