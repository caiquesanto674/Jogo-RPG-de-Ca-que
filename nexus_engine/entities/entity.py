"""
Módulo da Entidade base para o Nexus Engine.
"""

import uuid
from typing import Any, Dict, List

from nexus_engine.core.exceptions import EntityError
from nexus_engine.systems.energy_system import EnergiaUniversal

class Entidade:
    """
    Classe base para todas as entidades do jogo.
    """

    def __init__(self, nome: str, nivel: int = 1, hp_base: float = 100.0, energia_base: float = 500.0):
        if not nome:
            raise EntityError("Nome da entidade é obrigatório")
        if nivel < 1:
            raise EntityError("Nível deve ser pelo menos 1")

        self.id = str(uuid.uuid4())
        self.nome = nome
        self.nivel = nivel
        self.hp_maximo = hp_base + nivel * 10
        self.hp = self.hp_maximo
        self.energia = EnergiaUniversal(maxima=energia_base + nivel * 25)
        self.inventario: List[str] = []
        self.afeto = 0.0
        self.volicao = 1.0
        self.habilidades: List[str] = []

    def receber_dano(self, valor: float) -> float:
        """
        Recebe dano na entidade.
        """
        if self.esta_morta():
            return 0.0

        if valor < 0:
            valor = 0

        dano_final = valor
        self.hp = max(0, self.hp - dano_final)
        return dano_final

    def curar(self, valor: float) -> float:
        """
        Cura a entidade.
        """
        if valor < 0:
            valor = 0

        if self.esta_morta():
            return 0.0

        hp_anterior = self.hp
        self.hp = min(self.hp_maximo, self.hp + valor)
        return self.hp - hp_anterior

    def esta_viva(self) -> bool:
        """Verifica se a entidade está viva"""
        return self.hp > 0

    def esta_morta(self) -> bool:
        """Verifica se a entidade está morta"""
        return not self.esta_viva()

    def alterar_afeto(self, delta: float) -> float:
        """
        Altera o nível de afeto.
        """
        self.afeto = max(-100.0, min(100.0, self.afeto + delta))
        return self.afeto

    def alterar_volicao(self, delta: float) -> float:
        """
        Altera o nível de volição.
        """
        self.volicao = max(0.1, min(10.0, self.volicao + delta))
        return self.volicao

    def obter_info(self) -> Dict[str, Any]:
        """Retorna informações da entidade"""
        return {
            "id": self.id,
            "nome": self.nome,
            "nivel": self.nivel,
            "hp": self.hp,
            "hp_maximo": self.hp_maximo,
            "energia": self.energia.obter_info()
        }
