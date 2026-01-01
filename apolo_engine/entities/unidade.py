from typing import Optional, Tuple

from ..systems.tecnologia import Tecnologia
from .classes import CLASSES_APOLO


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
        self._moral = moral
        self._tech = tech
        self._posicao = posicao
        self._poder_psicologico = poder_psicologico
        self._aliados_proximos = aliados_proximos

        # Cache para otimização de performance
        self._forca_belica_cache: Optional[float] = None
        self._cache_sujo = True  # Dirty flag

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
        Utiliza um cache para evitar recálculos desnecessários.
        """
        if not self._cache_sujo and self._forca_belica_cache is not None:
            return self._forca_belica_cache

        # Bônus de Tecnologia
        bonus_tech = 1.0
        if self.tech:
            if self.classe in ["Tanque", "Drone"] and self.tech.arvore.get("Plasma", 0) > 1:
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

        self._forca_belica_cache = forca_final
        self._cache_sujo = False
        return forca_final

    def exibir_poder(self):
        print(f"\n--- {self.nome} ({self.classe}) ---")
        print(f"FORÇA BÉLICA: {self.calcular_forca_belica():.2f} | Moral: {self.moral}")
        if self.poder_psicologico == "Comando":
            print(f"Bônus Comando (aliados): +{0.25 * self.aliados_proximos:.2f}")


    # Propriedades com setters para invalidar o cache
    @property
    def moral(self) -> int:
        """Nível de moral da unidade."""
        return self._moral

    @moral.setter
    def moral(self, value: int):
        if self._moral != value:
            self._moral = value
            self._cache_sujo = True

    @property
    def poder_psicologico(self) -> Optional[str]:
        """Poder psicológico da unidade."""
        return self._poder_psicologico

    @poder_psicologico.setter
    def poder_psicologico(self, value: Optional[str]):
        if self._poder_psicologico != value:
            self._poder_psicologico = value
            self._cache_sujo = True

    @property
    def aliados_proximos(self) -> int:
        """Número de aliados próximos."""
        return self._aliados_proximos

    @aliados_proximos.setter
    def aliados_proximos(self, value: int):
        if self._aliados_proximos != value:
            self._aliados_proximos = value
            self._cache_sujo = True

    @property
    def tech(self) -> Tecnologia:
        """Tecnologia disponível para a unidade."""
        return self._tech

    @tech.setter
    def tech(self, value: Tecnologia):
        if self._tech != value:
            self._tech = value
            self._cache_sujo = True

    @property
    def posicao(self) -> Optional[Tuple[int, int]]:
        """Posição tática da unidade."""
        return self._posicao

    @posicao.setter
    def posicao(self, value: Optional[Tuple[int, int]]):
        if self._posicao != value:
            self._posicao = value
            self._cache_sujo = True
