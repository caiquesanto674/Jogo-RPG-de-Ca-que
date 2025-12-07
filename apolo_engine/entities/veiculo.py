# entities/veiculo.py
import random, math
from typing import Tuple
from .entidade import Entidade

class VeiculoDeCombate(Entidade):
    def __init__(self, nome: str, tipo_arma: str, base, pos: Tuple[int,int], alcance_max: int = 5):
        super().__init__(nome, hp=500, pos=pos)
        self.tipo_arma = tipo_arma
        self.base_logistica = base
        self.municao = 10
        self.moral_tripulacao = 80
        self.alcance_max = alcance_max
        self.tipo_unidade = 'Veiculo'

    def mover(self, dx: int, dy: int, world_map):
        nx, ny = self.pos[0]+dx, self.pos[1]+dy
        modificador = world_map.get_modificador_movimento(self.pos, self.tipo_unidade)
        if modificador >= 0.5:
            self.pos = (nx, ny)
            return f"{self.nome} moveu para {self.pos} ({world_map.get_terreno_nome(self.pos)})"
        return f"{self.nome} falhou em se mover: terreno difícil."

    def atirar(self, alvo, world_map):
        distancia = math.hypot(self.pos[0]-alvo.pos[0], self.pos[1]-alvo.pos[1])
        if self.municao > 0 and distancia <= self.alcance_max:
            self.municao -= 1
            dano = random.randint(50, 90)
            alvo.hp = max(0, alvo.hp - dano)
            self.base_logistica.recursos["Munição"] = max(0, self.base_logistica.recursos.get("Munição",0)-1)
            return f"{self.nome} atirou em {alvo.nome} e causou {dano} de dano."
        if distancia > self.alcance_max:
            return f"{self.nome}: alvo fora do alcance ({distancia:.1f})."
        return f"{self.nome}: sem munição."
