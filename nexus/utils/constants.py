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
