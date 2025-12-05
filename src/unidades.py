class Arma:
    def __init__(self, nome, poder, tipo): self.nome, self.poder, self.tipo = nome, poder, tipo
class Unidade:
    def __init__(self, nome, classe, forca, armas=None):
        self.nome, self.classe, self.forca = nome, classe, forca
        self.armas = armas if armas else []
    def poder_combate(self): return self.forca + sum(a.poder for a in self.armas)
class BaseMilitar:
    def __init__(self, nome): self.nome, self.defesa, self.unidades = nome, 120, []
    def adicionar_unidade(self, u): self.unidades.append(u)
