class Ambiente:
    """Simula o ambiente do mapa, ciclo dia/noite e recursos locais."""

    def __init__(self, nome: str, tipo: str, ciclo: str = "dia"):
        self.nome, self.tipo, self.ciclo = nome, tipo, ciclo
        self.recursos = {"agua": 1000, "mana": 350, "sombra": 0, "lux": 120}

    def atualizar(self):
        """Alterna ciclo e ajusta recursos (ex: mana, lux, sombra)."""
        self.ciclo = "noite" if self.ciclo == "dia" else "dia"
        if self.ciclo == "noite":
            self.recursos["lux"] = max(0, self.recursos["lux"] - 90)
            self.recursos["sombra"] += 5
        else:
            self.recursos["lux"] += 90
            self.recursos["sombra"] = max(0, self.recursos["sombra"] - 2)
