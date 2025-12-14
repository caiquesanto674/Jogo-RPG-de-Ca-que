from datetime import datetime
from typing import List

# AGENT-DEFINED: The forward declaration of BaseMilitar is necessary to avoid circular imports.
# This is a common practice in Python when two modules depend on each other.
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..entities.base import BaseMilitar

class Economia:
    def __init__(self, reserva=100000):
        self.reserva = reserva
        self.transacoes = []
        self.recursos_locais = {"metal": 2000, "combustivel": 1000, "plasma": 500}

    def transferir(self, valor: int, destino: str) -> bool:
        if valor <= self.reserva:
            self.reserva -= valor
            self.transacoes.append(
                {"destino": destino, "valor": valor, "timestamp": datetime.now()}
            )
            return True
        return False

    # AGENT-DEFINED: New method for dynamic income generation
    def gerar_renda_ciclo(self, bases: List['BaseMilitar']):
        """
        Gera renda com base na eficiência operacional de todas as bases militares.
        """
        renda_total = 0
        for base in bases:
            # AGENT-DEFINED: Income is proportional to the base's operational efficiency
            renda_base = int(1000 * base.nivel * base.eficiencia_operacional)
            renda_total += renda_base

        self.reserva += renda_total
        print(f"[ECONOMIA] Renda do ciclo: +{renda_total}. Reserva total: {self.reserva}")
