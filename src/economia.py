import random
import logging
from src.utils import frase_confirmacao

class Economia:
    """Gerenciamento da economia central do jogo: recursos, produção e inflação."""
    def __init__(self):
        self.recursos = {'ouro': 5000, 'aço': 3000, 'mana': 800, 'comida': 1500, 'energia': 900}
        self.producao = 2000
        self.inflacao = 1.0
    def operar(self):
        for k in self.recursos:
            if k != 'ouro': self.recursos[k] += self.producao // len(self.recursos)
        self.inflacao *= (0.99 + random.random() * 0.02)
        logging.info("[ECONOMIA] Produção e reservas atualizadas.")
    def comprar(self, recurso, qtd, custo_unit):
        custo = qtd * custo_unit
        if self.recursos.get('ouro',0) >= custo:
            self.recursos['ouro'] -= custo
            self.recursos[recurso] = self.recursos.get(recurso, 0) + qtd
            logging.info(frase_confirmacao("CORRECAO", True))
            return True
        logging.warning(frase_confirmacao("CORRECAO", False))
        return False
