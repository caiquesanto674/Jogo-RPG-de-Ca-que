import logging
from src.utils import frase_confirmacao

class SistemaAutoCorrecao:
    """Monitora e corrige automaticamente falhas graves de recursos."""
    def __init__(self, limite_comida=1000): self.limite_comida = limite_comida
    def monitorar(self, economia): return economia.recursos['comida'] < self.limite_comida
    def corrigir(self, economia):
        if self.monitorar(economia):
            sucesso = economia.comprar('comida', 1000, 1)
            logging.info(frase_confirmacao("CORRECAO", sucesso))
            return sucesso
        return True
