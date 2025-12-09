from enum import Enum

FRASES_CONFIRMACAO = {
    "MILITAR_SUCESSO": "Operação militar executada com êxito!",
    "MILITAR_FALHA": "Falha operacional. Perdas registradas.",
    "TECNOLOGIA_SUCESSO": "Upgrade tecnológico ativado.",
    "CORRECAO_SUCESSO": "AI: Bug crítico resolvido.",
    "CORRECAO_FALHA": "Auto-correção falhou. Recurso insuficiente.",
}


def frase_confirmacao(codigo, sucesso=True):
    key = f"{codigo}_{'SUCESSO' if sucesso else 'FALHA'}"
    return FRASES_CONFIRMACAO.get(key, "Ação processada.")


class EstadoComportamento(Enum):
    OFENSIVO = "OFENSIVO"
    DEFENSIVO = "DEFENSIVO"
    RECUADO = "RECUADO"
    AUTO_CORRECAO = "AUTO_CORRECAO"
    EXPLORACAO = "EXPLORACAO"
