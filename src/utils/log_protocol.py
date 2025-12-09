# src/utils/log_protocol.py

import hashlib
from datetime import datetime
from typing import Dict, List, Any

class ProtocoloConfirmacao:
    @staticmethod
    def gerar(acao: str, agente: str, nivel: int) -> str:
        s = f"{acao}|{agente}|{nivel}|{datetime.now().isoformat()}"
        return hashlib.sha256(s.encode()).hexdigest()

class LogSistema:
    def __init__(self):
        self.registros: List[Dict[str, Any]] = []
    def registrar(self, tipo: str, origem: str, conteudo: str):
        entrada = {'momento': datetime.now().isoformat(), 'tipo': tipo, 'origem': origem, 'conteudo': conteudo}
        self.registros.append(entrada)
        print(f"[{tipo.upper()}] ({origem}) {conteudo}")
