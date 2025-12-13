from datetime import datetime
from typing import Any


class LogGlobal:
    """Armazena todos os eventos importantes do jogo."""

    def __init__(self):
        self.registros = []

    def registrar(self, evento: str, args: Any):
        self.registros.append((datetime.now(), evento, args))
