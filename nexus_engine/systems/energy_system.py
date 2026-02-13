"""
Módulo do Sistema de Energia para o Nexus Engine.
"""

from datetime import datetime
from typing import Any, Dict

from nexus_engine.core.exceptions import EnergyError

class EnergiaUniversal:
    """
    Sistema de energia para entidades e habilidades.
    """

    def __init__(self, maxima: float = 1000.0, regeneracao: float = 5.0):
        if maxima <= 0:
            raise ValueError("Energia máxima deve ser positiva")
        if regeneracao < 0:
            raise ValueError("Regeneração não pode ser negativa")

        self.maxima = maxima
        self.atual = maxima
        self.regeneracao = regeneracao
        self.ultima_atualizacao = datetime.utcnow()

    def consumir(self, valor: float) -> bool:
        """
        Consome energia se disponível.
        """
        if valor < 0:
            raise EnergyError("Valor de consumo não pode ser negativo")

        self._atualizar_regeneracao()

        if valor <= self.atual:
            self.atual -= valor
            return True
        return False

    def _atualizar_regeneracao(self) -> None:
        """Atualiza energia baseado no tempo desde a última atualização"""
        agora = datetime.utcnow()
        delta = (agora - self.ultima_atualizacao).total_seconds()

        if delta > 0:
            regenerado = delta * self.regeneracao
            self.atual = min(self.maxima, self.atual + regenerado)
            self.ultima_atualizacao = agora

    def obter_info(self) -> Dict[str, Any]:
        """Retorna informações sobre a energia"""
        self._atualizar_regeneracao()
        return {
            "atual": self.atual,
            "maxima": self.maxima,
            "porcentagem": (self.atual / self.maxima) * 100 if self.maxima > 0 else 0,
        }
