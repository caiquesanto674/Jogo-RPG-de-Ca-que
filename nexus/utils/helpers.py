# nexus/utils/helpers.py
from datetime import datetime
from enum import Enum
from typing import Any


# === ENUMERADORES E CÓDIGOS DE CONFIRMAÇÃO ===
class EstadoAto(Enum):
    OFENSIVO = "OFENSIVO"
    DEFENSIVO = "DEFENSIVO"
    DIPLOMACIA = "DIPLOMACIA"
    SUPORTE = "SUPORTE"
    EXPLORACAO = "EXPLORACAO"


CODIGOS_CONFIRMACAO = {
    "MILITAR_SUCESSO": "Operação militar executada com êxito!",
    "MILITAR_FALHA": "Falha operacional. Perdas registradas.",
    "SUPORTE_SUCESSO": "Reforços e suporte enviados!",
    "TECNOLOGIA_SUCESSO": "Upgrade tecnológico ativado.",
    "EXPLORACAO_MUNDO": "Exploração iniciada.",
    "GUARDIAO_DESPERTAR": "Guardião despertado! Poder lendário ativo.",
}


def confirmar(codigo: str, sucesso: bool = True) -> str:
    """Retorna a frase de confirmação formatada."""
    key = f"{codigo}_{'SUCESSO' if sucesso else 'FALHA'}"
    return CODIGOS_CONFIRMACAO.get(key, "Ação processada.")


# ----------------------- SEÇÃO 1: CORE E INICIALIZAÇÃO -----------------------
def regra_base_global():
    """Define a regra fundamental do universo do jogo."""
    return "Volição Ativa e Kernel 2.5"


class LogGlobal:
    """Armazena todos os eventos importantes do jogo."""

    def __init__(self):
        self.registros = []

    def registrar(self, evento: str, args: Any):
        self.registros.append((datetime.now(), evento, args))
