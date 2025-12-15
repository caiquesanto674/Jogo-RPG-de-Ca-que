from typing import Optional, Tuple

from ..systems.tecnologia import Tecnologia
from .classes import CLASSES_APOLO


# ⚡ Bolt Optimization: Usando um set para verificação de classe O(1).
# Evita a criação de uma nova lista em cada chamada da função crítica de performance.
TECH_PLASMA_CLASSES = {"Tanque", "Drone"}


class UnidadeMilitar:
    def __init__(
        self,
        nome: str,
        classe: str,
        moral: int = 100,
        tech: Tecnologia = None,
        posicao: Optional[Tuple[int, int]] = None,
        poder_psicologico: Optional[str] = None,
        aliados_proximos: int = 0,
    ):
        # 1. Carrega o perfil da classe do dicionário
        perfil = CLASSES_APOLO.get(classe)
        if not perfil:
            raise ValueError(f"Classe '{classe}' desconhecida.")

        self.nome = nome
        self.classe = classe
        self.moral = moral
        self.tech = tech
        self.posicao = posicao
        self.poder_psicologico = poder_psicologico
        self.aliados_proximos = aliados_proximos

        # 2. Atributos Táticos (Herdados da Classe)
        self.vida_maxima = perfil["Defesa_Base"]
        self.vida_atual = self.vida_maxima
        self.forca_base = perfil["Forca_Base"]
        self.mobilidade = perfil["Mobilidade"]
        self.habilidade_especial = perfil["Habilidade_Especial"]

        # 3. Bônus Específicos da Classe
        self.alcance_bonus = perfil.get("Bonus_Alcance", 0)
        self.bonus_comando = perfil.get("Bonus_Comando", 0)

    def calcular_forca_belica(self, bonus_posicao: float = 0.0) -> float:
        """
        Calcula a Força Bélica final, integrando todos os sistemas:
        Classe, Moral, Tecnologia, Posição Tática e Bônus Psicológicos.
        """
        # Bônus de Tecnologia
        bonus_tech = 1.0
        if self.tech:
            # ⚡ Bolt Optimization: Checagem de pertinência em set é O(1) em média.
            if self.classe in TECH_PLASMA_CLASSES and self.tech.arvore.get("Plasma", 0) > 1:
                bonus_tech += self.tech.arvore["Plasma"] * 0.15
            elif self.tech.arvore.get("IA", 0) > 1:
                bonus_tech += self.tech.arvore["IA"] * 0.1

        # Bônus Psicológico e de Aliança
        bonus_psico = (
            self.aliados_proximos if self.poder_psicologico == "Comando" else 0
        ) * 0.25
        bonus_alianca = self.aliados_proximos * 5

        # Bônus Tático de Posição (do futuro GridCombat)
        bonus_tatico = 1.0 + bonus_posicao

        # Fórmula final consolidada
        forca_com_moral = self.forca_base * (self.moral / 100.0)
        forca_final = (
            forca_com_moral * bonus_tech * bonus_tatico
            + bonus_psico
            + bonus_alianca
        )
        return forca_final

    def exibir_poder(self):
        print(f"\n--- {self.nome} ({self.classe}) ---")
        print(f"FORÇA BÉLICA: {self.calcular_forca_belica():.2f} | Moral: {self.moral}")
        if self.poder_psicologico == "Comando":
            print(f"Bônus Comando (aliados): +{0.25 * self.aliados_proximos:.2f}")
