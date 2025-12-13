from typing import List

from nexus.componentes.entidades import Guardiao, UnidadeCombate


class EnergiaBase:
    def __init__(self, energia_total=1000):
        self.energia_total = energia_total
        self.energia_atual = energia_total

    def consumir(self, valor):
        if valor <= self.energia_atual:
            self.energia_atual -= valor
            return True
        return False

    def recarregar(self, valor):
        self.energia_atual = min(self.energia_total, self.energia_atual + valor)


class BaseMilitar:
    """Base de Operações, Defesa e Recrutamento."""

    def __init__(self, nome: str):
        self.nome = nome
        self.nivel = 1
        self.recursos = {"aço": 1000, "mana": 300, "populacao": 200}
        self.defesa = 120
        self.unidades: List[UnidadeCombate] = []
        self.guardioes: List[Guardiao] = []
        self.energia = EnergiaBase(2000)
        self.suprimentos = 500

    def adicionar_guardiao(self, guardiao: Guardiao):
        self.guardioes.append(guardiao)

    def consumir_suprimentos(self, valor):
        if valor <= self.suprimentos:
            self.suprimentos -= valor
            return True
        return False
