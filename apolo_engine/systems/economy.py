from datetime import datetime
from typing import List

# Evita o problema de importação circular com type hinting
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..entities.base import BaseMilitar


class Economia:
    def __init__(self, reserva=100000):
        self.reserva = reserva
        self.transacoes = []
        self.recursos_locais = {"metal": 2000, "combustivel": 1000, "plasma": 500}
        self.bases_militares: List["BaseMilitar"] = []

    def adicionar_base(self, base: "BaseMilitar"):
        """Registra uma base militar no sistema econômico."""
        if base not in self.bases_militares:
            self.bases_militares.append(base)
            print(f"[ECONOMIA] Base {base.local} adicionada ao sistema econômico.")

    def gerar_renda_ciclo(self):
        """
        Gera a renda passiva com base na eficiência das bases militares.
        Uma base operando a 100% de eficiência gera uma renda baseada em seu nível.
        """
        renda_total_ciclo = 0
        renda_base_por_nivel = 50  # Créditos por nível da base por ciclo

        for base in self.bases_militares:
            renda_da_base = (
                renda_base_por_nivel
                * base.nivel
                * (base.eficiencia_operacional / 100.0)
            )
            renda_total_ciclo += renda_da_base

        self.reserva += renda_total_ciclo
        print(f"[ECONOMIA] Renda do ciclo: +{renda_total_ciclo:.2f}. Reserva atual: {self.reserva:.2f}")

    def transferir(self, valor: int, destino: str) -> bool:
        if valor <= self.reserva:
            self.reserva -= valor
            self.transacoes.append(
                {"destino": destino, "valor": valor, "timestamp": datetime.now()}
            )
            return True
        return False
