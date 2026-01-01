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
    def __init__(self, min_level: LogLevel = LogLevel.INFO):
        self.registros = []
        self.min_level = min_level

    def registrar(self, tipo, origem, conteudo, level: LogLevel = LogLevel.INFO):
        entrada = {
            "momento": datetime.now().isoformat(),
            "tipo": tipo,
            "origem": origem,
            "conteudo": conteudo,
            "level": level.name,
        }
        self.registros.append(entrada)

        if level.value >= self.min_level.value:
            print(f"[{level.name}] [{tipo}] {origem}: {conteudo}")
