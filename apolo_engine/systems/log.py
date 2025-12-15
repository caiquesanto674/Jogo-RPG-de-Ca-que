import hashlib
from datetime import datetime
from enum import Enum


class LogLevel(Enum):
    """Define os níveis de log para o sistema."""
    DEBUG = 1  # Informações detalhadas para desenvolvimento
    INFO = 2   # Eventos importantes e fluxo geral


class ProtocoloConfirmacao:
    @staticmethod
    def gerar(acao, agente, nivel):
        s = f"{acao}|{agente}|{nivel}|{datetime.now().isoformat()}"
        return hashlib.sha256(s.encode()).hexdigest()


class LogSistema:
    def __init__(self, nivel_minimo=LogLevel.INFO):
        self.registros = []
        self.nivel_minimo = nivel_minimo

    def registrar(self, tipo, origem, conteudo, nivel=LogLevel.INFO):
        """
        Registra uma entrada de log, mas só a exibe no console se o nível for
        adequado ao nível mínimo configurado.
        """
        entrada = {
            "momento": datetime.now().isoformat(),
            "tipo": tipo,
            "origem": origem,
            "conteudo": conteudo,
            "nivel": nivel.name
        }
        self.registros.append(entrada)

        # Controle de visibilidade: só imprime se o nível for suficiente
        if nivel.value >= self.nivel_minimo.value:
            print(f"[{tipo}] {origem}: {conteudo}")
