"""
Módulo Principal do Nexus Engine.
"""

from datetime import datetime
from typing import Any, Dict, Optional

from nexus_engine.core.logger import UniversalLog
from nexus_engine.core.event_manager import GerenciadorEventos
from nexus_engine.core.time_manager import NexusTime
from nexus_engine.core.exceptions import NexusError, EntityError
from nexus_engine.entities.entity import Entidade

class NexusEngine:
    """
    Motor principal do jogo que coordena todos os sistemas.
    """

    def __init__(self):
        self.log = UniversalLog()
        self.eventos = GerenciadorEventos(self.log)
        self.tempo = NexusTime()
        self.entidades: Dict[str, Entidade] = {}
        self.iniciado = False

        self.log.registrar("NexusEngine", "inicializacao", {"versao": "3.0"})

    def iniciar(self) -> bool:
        """
        Inicia o motor do jogo.
        """
        if self.iniciado:
            return False

        self.iniciado = True
        self.log.registrar("NexusEngine", "inicio", {"tempo_jogo": self.tempo.tempo_jogo.isoformat()})
        return True

    def registrar_entidade(self, entidade: Entidade) -> str:
        """
        Registra uma entidade no motor.
        """
        if entidade.id in self.entidades:
            raise EntityError(f"Entidade {entidade.id} já está registrada")

        self.entidades[entidade.id] = entidade
        self.log.registrar("NexusEngine", "entidade_registrada", {"id": entidade.id, "nome": entidade.nome})
        return entidade.id

    def tick(self) -> Dict[str, Any]:
        """
        Executa um ciclo de atualização do motor.
        """
        if not self.iniciado:
            raise NexusError("Motor não iniciado")

        tempo_atual = self.tempo.tick()
        eventos_processados = self.eventos.processar_lote(100)

        for entidade in self.entidades.values():
            entidade.energia.regenerar()

        return {
            "tempo": tempo_atual.isoformat(),
            "eventos_processados": len(eventos_processados),
        }
