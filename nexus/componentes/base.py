import uuid
from typing import List

from nexus.sistemas.economy import Economia
from nexus.componentes.unidade import UnidadeMilitar


class BaseMilitar:
    def __init__(self, owner: str, local: str, economia: Economia, nivel: int = 1):
        self.id = uuid.uuid4()
        self.owner = owner
        self.local = local
        self.nivel = nivel
        self.recursos = {"metal": 1000, "combustível": 500, "plasma": 120}
        self.economia = economia
        self.unidades: List[UnidadeMilitar] = []

    def expande(self, recurso_base: str, valor_base: int, custo_credito: int) -> bool:
        if (
            self.recursos.get(recurso_base, 0) >= valor_base
            and self.economia.reserva >= custo_credito
        ):
            self.recursos[recurso_base] -= valor_base
            self.economia.transferir(custo_credito, f"Expansão {self.local}")
            self.nivel += 1
            print(f"[BASE] Upgrade: {self.local} -> Nível {self.nivel}")
            return True
        print("[FALHA] Recursos ou Créditos insuficientes.")
        return False
