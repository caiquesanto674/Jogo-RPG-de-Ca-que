import uuid
from typing import List

from ..systems.economy import Economia
from .unidade import UnidadeMilitar


class BaseMilitar:
    """
    Representa uma base militar autônoma que opera como um "organismo vivo",
    com metabolismo, saúde e capacidade de decisão.
    """

    def __init__(self, owner: str, local: str, economia: Economia, nivel: int = 1):
        self.id = uuid.uuid4()
        self.owner = owner
        self.local = local
        self.nivel = nivel
        self.recursos = {"metal": 1000, "combustível": 500, "plasma": 120}
        self.economia = economia
        self.unidades: List[UnidadeMilitar] = []

        # Atributos vitais da base como "organismo"
        self.saude_base = 100.0  # Saúde estrutural e moral da base
        self.eficiencia_operacional = (
            1.0  # Multiplicador para performance (0.0 a 1.0)
        )

    def expande(self, recurso_base: str, valor_base: int, custo_credito: int) -> bool:
        if (
            self.recursos.get(recurso_base, 0) >= valor_base
            and self.economia.reserva >= custo_credito
        ):
            self.recursos[recurso_base] -= valor_base
            self.economia.transferir(custo_credito, f"Expansão {self.local}")
            self.nivel += 1
            print(f"📈 [EXPANSÃO] Base {self.local} evoluiu para o Nível {self.nivel}.")
            return True
        print(f"📉 [FALHA EXPANSÃO] Recursos ou créditos insuficientes para {self.local}.")
        return False

    def metabolismo_ciclo(self):
        """
        Consome recursos para manutenção (subsistência).
        Falhas degradam a saúde e eficiência da base.
        Este é o "coração" da base como organismo vivo.
        """
        custo_subsistencia = self.nivel * 150 + len(self.unidades) * 50
        print(
            f"❤️‍🩹 [METABOLISMO] Base {self.local} | Custo de Subsistência: {custo_subsistencia}"
        )

        if self.economia.transferir(
            custo_subsistencia, f"Subsistência {self.local}"
        ):
            print(f"✅ [SUCESSO] Subsistência da base {self.local} garantida.")
            # Regeneração leve se a subsistência for paga
            self.saude_base = min(100, self.saude_base + 2)
            self.eficiencia_operacional = min(1.0, self.eficiencia_operacional + 0.05)
        else:
            print(f"🚨 [FALHA SUBSISTÊNCIA] Base {self.local} sofre penalidades.")
            self.saude_base -= 10
            self.eficiencia_operacional -= 0.1
            print(
                f"💔 [ESTADO] Saúde: {self.saude_base:.1f}% | Eficiência: {self.eficiencia_operacional:.1f}%"
            )
