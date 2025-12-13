"""
Módulo de Log Universal para o Nexus Engine.
"""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from dataclasses import dataclass

@dataclass
class LogEntry:
    """Estrutura de dados para entrada de log"""
    id: str
    origem: str
    tipo: str
    dados: Dict[str, Any]
    timestamp: str

    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        return {
            "id": self.id,
            "origem": self.origem,
            "tipo": self.tipo,
            "dados": self.dados,
            "timestamp": self.timestamp
        }

class UniversalLog:
    """
    Sistema de log centralizado com limite de tamanho e filtros.

    Attributes:
        max_size (int): Número máximo de entradas no log
        eventos (List[LogEntry]): Lista de eventos registrados
    """

    def __init__(self, max_size: int = 5000):
        """
        Inicializa o sistema de log.

        Args:
            max_size: Número máximo de entradas no log (padrão: 5000)
        """
        self.max_size = max_size
        self.eventos: List[LogEntry] = []

    def registrar(self, origem: str, tipo: str, dados: Dict[str, Any]) -> str:
        """
        Registra um novo evento no log.

        Args:
            origem: Origem do evento
            tipo: Tipo do evento
            dados: Dados do evento

        Returns:
            str: ID do evento registrado

        Raises:
            ValueError: Se origem ou tipo forem vazios
        """
        if not origem or not tipo:
            raise ValueError("Origem e tipo são obrigatórios")

        evento_id = str(uuid.uuid4())
        entrada = LogEntry(
            id=evento_id,
            origem=origem,
            tipo=tipo,
            dados=dados,
            timestamp=datetime.utcnow().isoformat()
        )

        self.eventos.append(entrada)

        # Mantém o tamanho máximo
        if len(self.eventos) > self.max_size:
            self.eventos = self.eventos[-self.max_size:]

        return evento_id

    def consultar(self, tipo: Optional[str] = None,
                  origem: Optional[str] = None,
                  limite: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Consulta eventos no log com filtros.
        """
        resultados = self.eventos

        if tipo:
            resultados = [e for e in resultados if e.tipo == tipo]

        if origem:
            resultados = [e for e in resultados if e.origem == origem]

        if limite and limite > 0:
            resultados = resultados[-limite:]

        return [e.to_dict() for e in resultados]

    def limpar(self, manter_ultimos: Optional[int] = None) -> int:
        """
        Limpa o log.
        """
        if manter_ultimos:
            removidos = len(self.eventos) - manter_ultimos
            self.eventos = self.eventos[-manter_ultimos:]
            return max(0, removidos)
        else:
            removidos = len(self.eventos)
            self.eventos.clear()
            return removidos

    def estatisticas(self) -> Dict[str, Any]:
        """Retorna estatísticas do log"""
        tipos = {}
        origens = {}

        for evento in self.eventos:
            tipos[evento.tipo] = tipos.get(evento.tipo, 0) + 1
            origens[evento.origem] = origens.get(evento.origem, 0) + 1

        return {
            "total": len(self.eventos),
            "tipos": tipos,
            "origens": origens,
            "mais_recente": self.eventos[-1].timestamp if self.eventos else None
        }
