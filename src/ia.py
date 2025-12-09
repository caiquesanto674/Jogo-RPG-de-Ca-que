class AI_NPC:
    """NPC controlado por IA: auto-supervisão, reforço e supervisionado."""
    def __init__(self, nome, perfil="neutro"):
        self.nome = nome
        self.perfil = perfil
        self.evo = 0

    def calcular_poder(self):
        return 100 + self.evo * 10

    def agir(self, ambiente, contexto, forca_jogador=0):
        self.auto_supervisao(ambiente)
        poder_npc = self.calcular_poder()
        acao = self.supervisionado(contexto, forca_jogador, poder_npc)
        recompensa = 0
        if acao == "Ofensivo total":
            recompensa = 10
        elif acao == "Defensivo":
            recompensa = 5
        elif acao == "Recuo/Estratégia":
            recompensa = -3
        self.reforco(acao, recompensa)
        return f"{self.nome} age: {acao} (Nv AI {self.evo})"

    def auto_supervisao(self, ambiente):
        if ambiente.get('mana', 0) > 500:
            self.perfil = "alerta"
            self.evo += 2

    def supervisionado(self, contexto, forca_jogador, poder_npc):
        if contexto == "combate":
            if forca_jogador > poder_npc * 1.5:
                return "Recuo/Estratégia"
            elif forca_jogador > poder_npc:
                return "Defensivo"
            else:
                return "Ofensivo total"
        elif contexto == "crise":
            return "Recuo/Estratégia"
        return "Patrulha"

    def reforco(self, acao, recompensa):
        self.evo += recompensa // 5
        if self.evo < 0:
            self.evo = 0
