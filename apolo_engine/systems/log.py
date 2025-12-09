import hashlib
from datetime import datetime


class ProtocoloConfirmacao:
    @staticmethod
    def gerar(acao, agente, nivel):
        s = f"{acao}|{agente}|{nivel}|{datetime.now().isoformat()}"
        return hashlib.sha256(s.encode()).hexdigest()


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
        print(f"[{tipo}] {origem}: {conteudo}")
