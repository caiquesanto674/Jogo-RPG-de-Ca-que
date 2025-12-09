class Arma:
    def __init__(self, nome, poder, tipo): self.nome, self.poder, self.tipo = nome, poder, tipo
class Unidade:
    def __init__(self, nome, classe, forca, armas=None):
        self.nome, self.classe, self.forca = nome, classe, forca
        self.armas = armas if armas else []
    def poder_combate(self): return self.forca + sum(a.poder for a in self.armas)
class BaseMilitar:
    def __init__(self, nome):
        self.nome = nome
        self.defesa = 120
        self.unidades = []
        self.aliados = 0

    def adicionar_unidade(self, u):
        self.unidades.append(u)

    def calcular_forca_belica_total(self):
        poder_base = sum(u.poder_combate() for u in self.unidades)
        bonus_aliados = (1.05) ** self.aliados
        return poder_base * bonus_aliados
