from nexus.sistemas.tecnologia import Tecnologia


class AI_NPC:
    def __init__(self, nome: str, personalidade: str, nivel: int, tech: Tecnologia):
        self.nome = nome
        self.personalidade = personalidade
        self.nivel = nivel
        self.tech = tech
        self.registro_acoes = []

    def decisao(self, forca_do_jogador: float) -> str:
        if forca_do_jogador > 200 * self.nivel:
            acao = "negociar" if self.personalidade == "analítico" else "defender"
        elif forca_do_jogador > 120 * self.nivel:
            acao = "explorar"
        else:
            acao = "atacar"
        self.registro_acoes.append((forca_do_jogador, acao))
        return acao

    def frase_comportamental(self, acao: str, forca: float) -> str:
        frases = {
            "atacar": f"🚨 {self.nome}: ATAQUE TOTAL! Plasma N{self.tech.arvore['Plasma']}",
            "defender": f"🛡️ {self.nome}: Posições defensivas reforçadas.",
            "negociar": f"🤝 {self.nome}: Propondo aliança estratégica.",
            "explorar": f"🗺️ {self.nome}: Mapeando recursos críticos.",
        }
        return frases.get(acao, "Aguardando análise...")
