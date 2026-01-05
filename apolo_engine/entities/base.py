import uuid
from typing import List

from ..systems.economy import Economia
from .unidade import UnidadeMilitar
from ..systems.log import LogSistema


class BaseMilitar:
    def __init__(
        self, owner: str, local: str, economia: Economia, log: LogSistema, nivel: int = 1
    ):
        self.id = uuid.uuid4()
        self.owner = owner
        self.local = local
        self.nivel = nivel
        self.recursos = {"metal": 1000, "combustível": 500, "plasma": 120}
        self.economia = economia
        self.log = log
        self.unidades: List[UnidadeMilitar] = []

    def expande(self, recurso_base: str, valor_base: int, custo_credito: int) -> bool:
        if (
            self.recursos.get(recurso_base, 0) >= valor_base
            and self.economia.reserva >= custo_credito
        ):
            self.recursos[recurso_base] -= valor_base
            self.economia.transferir(custo_credito, f"Expansão {self.local}")
            self.nivel += 1
            self.log.registrar(
                "BASE", self.owner, f"Upgrade: {self.local} -> Nível {self.nivel}"
            )
            return True
        self.log.registrar(
            "FALHA", self.owner, "Recursos ou Créditos insuficientes."
        )
        return False
