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
        self.moral = moral  # Usa o setter da property
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
        # Cache para otimização de performance
        self._forca_belica_cache: Optional[float] = None
        self._cache_is_dirty: bool = True

    @property
    def moral(self) -> int:
        return self._moral

    @moral.setter
    def moral(self, value: int):
        self._moral = value
        self.invalidate_cache()

    def invalidate_cache(self):
        """Marca o cache como sujo para forçar o recálculo."""
        self._cache_is_dirty = True

    def _recalculate_forca_belica(self, bonus_posicao: float) -> float:
        """Lógica de cálculo real da Força Bélica."""
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
        forca_com_moral = self.forca_base * (self._moral / 100.0)
        forca_final = (
            forca_com_moral * bonus_tech * bonus_tatico
            + bonus_psico
            + bonus_alianca
        )
        return forca_final

    def calcular_forca_belica(self, bonus_posicao: float = 0.0) -> float:
        """
        Calcula a Força Bélica final. Usa um cache para o caso base (sem bônus),
        mas recalcula se um bônus de posição for fornecido.
        """
        # ⚡ Bolt: Se houver bônus de posição, o cache é ignorado para garantir a precisão.
        if bonus_posicao != 0.0:
            return self._recalculate_forca_belica(bonus_posicao)

        # ⚡ Bolt: Usa o cache apenas para o cálculo padrão (sem bônus de posição)
        if not self._cache_is_dirty and self._forca_belica_cache is not None:
            return self._forca_belica_cache

        # Calcula, armazena em cache e retorna
        self._forca_belica_cache = self._recalculate_forca_belica(0.0)
        self._cache_is_dirty = False
        return self._forca_belica_cache

    def exibir_poder(self):
        print(f"\n--- {self.nome} ({self.classe}) ---")
        print(f"FORÇA BÉLICA: {self.calcular_forca_belica():.2f} | Moral: {self.moral}")
        if self.poder_psicologico == "Comando":
            print(f"Bônus Comando (aliados): +{0.25 * self.aliados_proximos:.2f}")
