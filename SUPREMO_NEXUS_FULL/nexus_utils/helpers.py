def rank_xp(xp):
    limites = [100, 500, 1000, 2500, 8000, 18000, 30000, 70000, 99999999]
    tags = ['F', 'E', 'D', 'C', 'B', 'A', 'S', 'SS', 'Lenda']
    for i, v in enumerate(limites):
        if xp < v:
            return tags[i]
    return tags[-1]


def frase_confirmacao(personagem, acao, sucesso=True, cor="\u001B[92m"):
    status = "Sucesso" if sucesso else "Falha"
    return f"{cor}[{personagem.nome}-{personagem.cargo}] {acao} - {status}\u001B[0m"
