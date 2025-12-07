# entities/entidade.py
import random
from typing import Optional, Tuple

class Entidade:
    def __init__(self, nome: str, hp: int, pos: Tuple[int,int]=(0,0)):
        self.nome = nome
        self.hp = hp
        self.pos = pos
        self.inventario = []

class Personagem(Entidade):
    def __init__(self, nome: str, cargo='Jogador', raca='Humano', classe='Guerreiro'):
        super().__init__(nome, hp=100, pos=(0,0))
        self.cargo = cargo
        self.moral = 100.0 if cargo != 'OWNER' else None
        self.humor = "neutro"
        self.base = None

    def agir(self, acao: str, alvo: Optional[Entidade] = None):
        if acao == 'atacar' and alvo:
            dano = random.randint(10, 30)
            alvo.hp = max(0, alvo.hp - dano)
            return f"{self.nome} ataca {alvo.nome} e causa {dano} de dano."
        return f"{self.nome} executou: {acao}"

class MonarcaAbsoluto(Personagem):
    def __init__(self, nome: str, base):
        super().__init__(nome, cargo="OWNER")
        self.moral = 100.0
        self.indice_dimensional = 3.0
        self.hp = 9999
        self.base = base
        self.ativacao_overflow = False

    def ativar_volicao(self):
        if self.moral < 20 and not self.ativacao_overflow:
            self.indice_dimensional += 0.5
            self.moral = 70
            self.ativacao_overflow = True
            return True
        return False

class Inimigo(Personagem):
    def __init__(self, nome: str, nivel_ameaca=90, poder_psicologico=True, pos=(10,10)):
        super().__init__(nome, cargo='INIMIGO', raca='Demônio', classe='Mago')
        self.hp = 150
        self.nivel_forca = nivel_ameaca
        self.poder_psicologico = poder_psicologico
        self.pos = pos

    def usar_poder(self, alvo: MonarcaAbsoluto):
        """Ataque psicológico com mitigação pela base (defesa_psiquica)."""
        if self.poder_psicologico and alvo.base:
            dano_base = self.nivel_forca * 0.75
            defesa_pct = getattr(alvo.base, "defesa_psiquica", 0.0)
            dano_final = dano_base * (1.0 - defesa_pct)
            alvo.moral = max(0.0, alvo.moral - dano_final)
            alvo.humor = "dominado_psicologicamente"
            return {'tipo': 'PSICOLOGICO', 'valor': dano_final}
        return {'tipo': 'IDLE', 'valor': 0}
