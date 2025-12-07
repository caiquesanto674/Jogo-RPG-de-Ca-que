class AI_NPC:
    """NPC controlado por IA: auto-supervisão, reforço e supervisionado."""
    def __init__(self, nome, perfil="neutro"): self.nome, self.perfil, self.evo = nome, perfil, 0
    def agir(self, ambiente, contexto):
        self.auto_supervisao(ambiente)
        acao = self.supervisionado(contexto)
        self.reforco(acao, 10 if acao=="Ofensivo total" else -3)
        return f"{self.nome} age: {acao} (Nv AI {self.evo})"
    def auto_supervisao(self, ambiente):
        if ambiente.get('mana',0)>500: self.perfil, self.evo = "alerta", self.evo+2
    def supervisionado(self, contexto):
        if contexto=="combate": return "Ofensivo total"
        elif contexto=="crise": return "Recuo/Estratégia"
        return "Patrulha"
    def reforco(self, acao, recompensa): self.evo += recompensa//5
