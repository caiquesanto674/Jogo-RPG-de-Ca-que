from datetime import datetime
from typing import List


class Economia:
    """
    Sistema econômico centralizado que gerencia a reserva de créditos
    e a geração de renda a cada ciclo.
    """

    def __init__(self, reserva=100000):
        self.reserva = reserva
        self.transacoes = []
        self.recursos_locais = {"metal": 2000, "combustivel": 1000, "plasma": 500}

    def transferir(self, valor: int, destino: str) -> bool:
        """Transfere um valor da reserva para um destino, se houver fundos."""
        if valor <= self.reserva:
            self.reserva -= valor
            self.transacoes.append(
                {"destino": destino, "valor": valor, "timestamp": datetime.now()}
            )
            return True
        return False

    def gerar_renda_ciclo(self, bases: List) -> int:
        """
        Gera renda com base na eficiência operacional de todas as bases.
        Uma base com 100% de eficiência contribui mais para a economia.
        """
        renda_total = 0
        for base in bases:
            # A renda de cada base é seu nível * um fator, modulado pela eficiência
            renda_base = base.nivel * 500 * base.eficiencia_operacional
            renda_total += renda_base

        self.reserva += int(renda_total)
        print(
            f"💰 [ECONOMIA] Renda do ciclo gerada: {int(renda_total):,} créditos. Reserva atual: {self.reserva:,}"
        )
        return int(renda_total)
