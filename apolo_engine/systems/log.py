import hashlib
import secrets
from datetime import datetime


class ProtocoloConfirmacao:
    @staticmethod
    def gerar(acao, agente, nivel):
        salt = secrets.token_hex(16)
        s = f"{salt}|{acao}|{agente}|{nivel}|{datetime.now().isoformat()}"
        return hashlib.sha256(s.encode()).hexdigest()


class Cores:
    """Códigos de cores ANSI para o terminal."""
    VERDE = '\033[92m'
    AMARELO = '\033[93m'
    VERMELHO = '\033[91m'
    AZUL = '\033[94m'
    CIANO = '\033[96m'
    FIM = '\033[0m'

class LogSistema:
    def __init__(self):
        self.registros = []

    def registrar(self, tipo, origem, conteudo):
        entrada = {
            "momento": datetime.now().isoformat(),
            "tipo": tipo,
            "origem": origem,
            "conteudo": conteudo,
        }
        self.registros.append(entrada)

        cor_map = {
            "PODER": Cores.AMARELO,
            "IA": Cores.VERMELHO,
            "PROTOCOLO": Cores.AZUL,
            "BASE": Cores.VERDE,
            "FALHA": Cores.VERMELHO,
        }
        cor = cor_map.get(tipo, Cores.FIM)

        print(f"{cor}[{tipo}]{Cores.FIM} {origem}: {conteudo}")
