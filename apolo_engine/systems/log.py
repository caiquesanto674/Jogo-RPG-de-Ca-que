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
    def __init__(self, min_level=LogLevel.INFO):
        self.registros = []
        self.min_level = min_level

    def registrar(self, tipo, origem, conteudo, level=LogLevel.INFO):
        if level.value >= self.min_level.value:
            entrada = {
                "momento": datetime.now().isoformat(),
                "tipo": tipo,
                "origem": origem,
                "conteudo": conteudo,
                "level": level.name,
            }
            self.registros.append(entrada)
            print(f"[{level.name}] [{tipo}] {origem}: {conteudo}")
