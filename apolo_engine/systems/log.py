import hashlib
import secrets
from datetime import datetime
from enum import Enum


class LogLevel(Enum):
    DEBUG = 1
    INFO = 2


class ProtocoloConfirmacao:
    @staticmethod
    def gerar(acao, agente, nivel):
        salt = secrets.token_hex(16)
        s = f"{salt}|{acao}|{agente}|{nivel}|{datetime.now().isoformat()}"
        return hashlib.sha256(s.encode()).hexdigest()


class LogSistema:
    def __init__(self, min_level=LogLevel.INFO):
        self.registros = []
        self.min_level = min_level

    def registrar(self, tipo, origem, conteudo, level=LogLevel.INFO):
        entrada = {
            "momento": datetime.now().isoformat(),
            "tipo": tipo,
            "origem": origem,
            "conteudo": conteudo,
            "level": level.name,
        }
        self.registros.append(entrada)

        if level.value >= self.min_level.value:
            print(f"[{tipo}] {origem}: {conteudo}")
