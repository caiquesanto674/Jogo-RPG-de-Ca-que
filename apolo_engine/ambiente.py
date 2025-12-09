class Ambiente:
    def __init__(self, nome, tipo, ciclo="dia"):
        self.nome, self.tipo, self.ciclo = nome, tipo, ciclo
        self.recursos = {"agua": 1000, "mana": 350, "sombra": 0, "lux": 120}

    def atualizar(self):
        self.ciclo = "noite" if self.ciclo == "dia" else "dia"
