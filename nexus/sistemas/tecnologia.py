import logging

from nexus.utils.constants import confirmar


class Tecnologia:
    """Gerencia o nível tecnológico e desbloqueios."""

    def __init__(self):
        self.nivel = 1
        self.buffs = []
        self.descobertas = []

    def pesquisar(self, tema: str):
        self.nivel += 1
        self.descobertas.append(tema)
        logging.info(f"[TECH] Nova pesquisa: {tema} (nível {self.nivel})")
        logging.info(confirmar("TECNOLOGIA", True))
