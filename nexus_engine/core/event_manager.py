"""
Módulo de Gerenciamento de Eventos para o Nexus Engine.
"""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field

from nexus_engine.core.logger import UniversalLog

@dataclass
class Evento:
    """Representa um evento no sistema"""
    nome: str
    origem: str
    gravidade: int = 1
    dados: Dict[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    tempo: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self):
        """Validação após inicialização"""
        if self.gravidade < 1 or self.gravidade > 10:
            raise ValueError("Gravidade deve estar entre 1 e 10")

    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        return {
            "id": self.id,
            "nome": self.nome,
            "origem": self.origem,
            "gravidade": self.gravidade,
            "dados": self.dados,
            "tempo": self.tempo.isoformat()
        }

class GerenciadorEventos:
    """
    Gerencia fila de eventos com processamento em lote.
    """

    def __init__(self, log: UniversalLog):
        self.fila: List[Evento] = []
        self.log = log

    def disparar(self, evento: Evento) -> str:
        """
        Adiciona um evento à fila para processamento.
        """
        if not isinstance(evento, Evento):
            raise ValueError("Evento deve ser uma instância da classe Evento")

        self.fila.append(evento)
        self.log.registrar(
            origem=evento.origem,
            tipo="evento_disparado",
            dados=evento.to_dict()
        )

        return evento.id

    def processar_lote(self, tamanho_maximo: Optional[int] = None) -> List[Evento]:
        """
        Processa um lote de eventos da fila.
        """
        if not self.fila:
            return []

        if tamanho_maximo and tamanho_maximo > 0:
            lote = self.fila[:tamanho_maximo]
            self.fila = self.fila[tamanho_maximo:]
        else:
            lote = self.fila.copy()
            self.fila.clear()

        for evento in lote:
            self.log.registrar(
                origem="GerenciadorEventos",
                tipo="evento_processado",
                dados=evento.to_dict()
            )

        return lote

    def estatisticas(self) -> Dict[str, Any]:
        """Retorna estatísticas da fila de eventos"""
        gravidades = {}
        for evento in self.fila:
            gravidades[evento.gravidade] = gravidades.get(evento.gravidade, 0) + 1

        return {
            "tamanho_fila": len(self.fila),
            "distribuicao_gravidade": gravidades
        }
