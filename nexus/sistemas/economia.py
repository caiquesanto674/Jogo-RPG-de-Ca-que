import logging
import random


class Economia:
    """Gerencia reservas, produção e inflação dinâmica do jogo (Mecânica Tycoon)."""

    def __init__(self):
        self.reservas = {"ouro": 5000, "aço": 3000, "mana": 800, "comida": 1500, "energia": 900}
        self.producao_base = 2000
        self.inflacao = 1.0  # Base 1.0

    def operar(self):
        """Calcula produção e atualiza inflação."""
        producao_ajustada = int(
            self.producao_base * (2.0 - self.inflacao)
        )  # Penaliza com inflação alta
        if producao_ajustada < 0:
            producao_ajustada = 100

        for rec in self.reservas:
            self.reservas[rec] += int(producao_ajustada // len(self.reservas))

        # Inflação dinâmica: Varia 0.99 a 1.02 por turno
        self.inflacao *= 0.99 + random.random() * 0.03
        logging.info(f"[ECONOMIA] Reservas atualizadas. Inflação: {self.inflacao:.2f}")
