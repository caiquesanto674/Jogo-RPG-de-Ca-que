import hashlib
from datetime import datetime
from enum import Enum


class LogLevel(Enum):
    DEBUG = 1
    INFO = 2


class ProtocoloConfirmacao:
    @staticmethod
    def gerar(acao, agente, nivel):
        s = f"{acao}|{agente}|{nivel}|{datetime.now().isoformat()}"
        return hashlib.sha256(s.encode()).hexdigest()


class LogSistema:
    def __init__(self, level=LogLevel.INFO):
        self.registros = []
        self.level = level

    def registrar(self, level, tipo, origem, conteudo):
        if level.value < self.level.value:
            return

        entrada = {
            "momento": datetime.now().isoformat(),
            "tipo": tipo,
            "origem": origem,
            "conteudo": conteudo,
        }
        self.registros.append(entrada)
        print(f"[{tipo}] {origem}: {conteudo}")
