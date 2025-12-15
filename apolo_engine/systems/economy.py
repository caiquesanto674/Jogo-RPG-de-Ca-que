from __future__ import annotations
from datetime import datetime
from typing import List, TYPE_CHECKING

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

    def gerar_renda_ciclo(self, bases: List[BaseMilitar]):
        """
        Calcula e adiciona a renda gerada por todas as bases.
        A renda é proporcional à eficiência operacional de cada base.
        """
        renda_total = 0
        for base in bases:
            renda_base = 2500 * base.nivel * base.eficiencia_operacional
            renda_total += renda_base

        self.reserva += renda_total
        print(
            f"[ECONOMIA] Renda do ciclo: R$ {renda_total:,.0f}. Reserva atual: R$ {self.reserva:,.0f}"
        )
