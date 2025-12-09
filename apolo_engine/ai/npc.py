# apolo_engine/ai/npc.py

from apolo_engine.systems.tecnologia import ArvoreTecnologia


class AI_NPC:
    """
    Classe base para NPCs, IA de Combate e Entidades de Suporte.
    """

    def __init__(self, nome: str, arvore_tecnologia: ArvoreTecnologia):
        self.nome = nome
        self._tecnologia = arvore_tecnologia
        self.comportamento = "Patrulha"
        self.memoria_curta_prazo = []
        self.aliado_humanoide = False

    def decidir_acao_combate(self, alvo: object) -> str:
        """
        Lógica de decisão complexa (Modelo de Evolução Reativa).
        Analisa a situação e o nível de tecnologia para tomar a melhor decisão tática.
        """
        if (
            hasattr(alvo, "vida_atual")
            and hasattr(alvo, "vida_maxima")
            and alvo.vida_atual < alvo.vida_maxima * 0.3
            and self._tecnologia.pesquisas_desbloqueadas.get("TaticaOfensivaN2", False)
        ):
            self.comportamento = "Ofensiva Total"
            return "Atacar com habilidade especial Tática N2."
        if "dano massivo" in self.memoria_curta_prazo:
            self.comportamento = "Defensivo"
            return "Recuar e usar cobertura."
        else:
            self.comportamento = "Padrao"
            return "Ataque básico."

    def aprender_com_evento(self, evento: str):
        """Modelo de Evolução Ativa: Adiciona informações relevantes à memória para decisões futuras."""
        if "reforço inimigo" in evento:
            self.memoria_curta_prazo.append("necessidade de contra-reforço")
            print(f"IA {self.nome} aprendeu: {self.memoria_curta_prazo[-1]}")  # noqa: E501
