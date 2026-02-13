"""
Módulo de Gerenciamento de Tempo para o Nexus Engine.
"""

from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from nexus_engine.core.exceptions import TimeError

class NexusTime:
    """
    Sistema de tempo dinâmico para o jogo.
    """

    def __init__(self, tempo_inicial: Optional[datetime] = None):
        self.velocidade = 1.0
        self.tempo_jogo = tempo_inicial or datetime(3000, 1, 1, 0, 0, 0)
        self.ultimo_tick = datetime.utcnow()
        self.pausado = False

    def tick(self) -> datetime:
        """
        Atualiza o tempo do jogo baseado no tempo real.
        """
        if self.pausado:
            return self.tempo_jogo

        try:
            agora = datetime.utcnow()
            delta_real = (agora - self.ultimo_tick).total_seconds()
            self.ultimo_tick = agora

            delta_jogo = delta_real * self.velocidade
            self.tempo_jogo += timedelta(seconds=delta_jogo)

            return self.tempo_jogo
        except Exception as e:
            raise TimeError(f"Erro ao calcular tick de tempo: {str(e)}") from e

    def definir_velocidade(self, velocidade: float) -> None:
        """
        Define a velocidade do tempo.
        """
        if not 0.01 <= velocidade <= 50.0:
            raise ValueError("Velocidade deve estar entre 0.01 e 50.0")
        self.velocidade = velocidade

    def pausar(self) -> None:
        """Pausa o tempo do jogo"""
        self.pausado = True

    def retomar(self) -> None:
        """Retoma o tempo do jogo"""
        self.pausado = False
        self.ultimo_tick = datetime.utcnow()

    def obter_info(self) -> Dict[str, Any]:
        """Retorna informações sobre o estado do tempo"""
        return {
            "tempo_jogo": self.tempo_jogo.isoformat(),
            "velocidade": self.velocidade,
            "pausado": self.pausado,
        }
