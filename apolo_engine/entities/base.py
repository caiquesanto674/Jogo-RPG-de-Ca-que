import uuid
from typing import List

from ..systems.economy import Economia
from .unidade import UnidadeMilitar
from ..systems.tecnologia import Tecnologia


class BaseMilitar:
    def __init__(self, owner: str, local: str, economia: Economia, nivel: int = 1):
        self.id = uuid.uuid4()
        self.owner = owner
        self.local = local
        self.nivel = nivel
        self.recursos = {"metal": 1000, "combustível": 500, "plasma": 120}
        self.economia = economia
        self.unidades: List[UnidadeMilitar] = []
        self.saude_base = 100.0
        self.eficiencia_operacional = 1.0

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

    def metabolismo_ciclo(self, tech: Tecnologia):
        """
        Calcula e processa o custo de subsistência da base por turno.
        Falhas em pagar o custo degradam a saúde e eficiência da base.
        """
        custo_base = 500 * self.nivel
        modificador_ia = 1 - (tech.arvore.get("IA", 1) * 0.05)
        custo_subsistencia = custo_base * modificador_ia

        pago = self.economia.transferir(
            custo_subsistencia, f"Subsistência {self.local}"
        )

        if pago:
            self.saude_base = min(100.0, self.saude_base + 2.5)
            self.eficiencia_operacional = min(1.0, self.eficiencia_operacional + 0.02)
            print(
                f"[BASE] {self.local} pagou R$ {custo_subsistencia:,.0f} de subsistência. Saúde: {self.saude_base:.1f}%, Eficiência: {self.eficiencia_operacional:.2f}"
            )
        else:
            self.saude_base = max(0.0, self.saude_base - 10)
            self.eficiencia_operacional = max(0.1, self.eficiencia_operacional - 0.05)
            print(
                f"[ALERTA] {self.local} FALHOU em pagar subsistência. Saúde: {self.saude_base:.1f}%, Eficiência: {self.eficiencia_operacional:.2f}"
            )
