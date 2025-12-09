from typing import Optional, Tuple

from ..systems.tecnologia import Tecnologia  # Importa a classe Tech (do código consolidado)
from .classes import CLASSES_APOLO  # Importa as novas classes


class UnidadeMilitar:
    def __init__(
        self,
        nome: str,
        classe: str,
        moral: int = 100,
        tech: Tecnologia = None,
        posicao: Optional[Tuple[int, int]] = None,
    ):
        # 1. Carrega o perfil da classe
        perfil = CLASSES_APOLO.get(classe)
        if not perfil:
            raise ValueError(f"Classe '{classe}' desconhecida.")

        self.nome = nome
        self.classe = classe
        self.moral = moral
        self.tech = tech

        # 2. Atributos Táticos (Herdados da Classe)
        self.vida_maxima = perfil["Defesa_Base"]
        self.vida_atual = self.vida_maxima
        self.forca_base = perfil["Forca_Base"]
        self.mobilidade = perfil["Mobilidade"]
        self.habilidade_especial = perfil["Habilidade_Especial"]

        # 3. Atributos de Posição
        self.posicao = posicao

        # Adiciona bônus específicos (ex: Franco-Atirador tem mais alcance, Comandante dá bônus)
        self.alcance_bonus = perfil.get("Bonus_Alcance", 0)
        self.bonus_comando = perfil.get("Bonus_Comando", 0)

    def calcular_forca_belica(self, bonus_posicao: float = 0.0) -> float:
        """
        Calcula a Força Bélica final, integrando Classe, Moral, Tecnologia e Posição.
        """

        # 1. Base + Moral
        forca_efetiva = self.forca_base * (self.moral / 100.0)

        # 2. Bônus de Tecnologia (Ex: +10% por nível de Plasma)
        bonus_tech = 1.0 + (self.tech.arvore.get("Plasma", 0) * 0.10 if self.tech else 0)

        # 3. Bônus Tático de Posição (do GridCombat)
        bonus_tatico = 1.0 + bonus_posicao

        # 4. Bônus de Comando (se for um Comandante)
        bonus_comando = 1.0 + self.bonus_comando

        return forca_efetiva * bonus_tech * bonus_tatico * bonus_comando
