# nexus/sistemas/ia.py
import logging
import random
from typing import Dict

# Importando as classes necessárias dos outros módulos
from ..componentes.entidades import BaseMilitar
from .mecanicas_jogo import Ambiente


class AI_NPC:
    """IA de suporte e narrativa (NPCs adaptativos / Ciel/Rafael / IA de SAO)."""

    def __init__(self, nome: str, comportamento: str = "normal"):
        self.nome, self.comportamento, self.evolucao = nome, comportamento, 0

    def auto_supervision(self, ambiente_recursos: Dict[str, int]):
        """Evolução ativa: Reage ao estado do mundo."""
        if ambiente_recursos.get("mana", 0) > 500:
            self.comportamento = "alerta estratégico"
            self.evolucao += 2

    def reinforcement(self, reward: int):
        """Evolução reativa: Aprende com o sucesso/falha de suas ações."""
        self.evolucao += reward

    def supervised(self, contexto: str) -> str:
        """Define a ação baseada no contexto (Lógica do Ciel/Rafael)."""
        if contexto == "combate":
            return "Ofensiva máxima (Foco: Alvos de maior ameaça)"
        elif contexto == "crise":
            return "Recuo Tático e Diplomacia de emergência"
        return "Patrulha padrão e coleta de dados"

    def agir(self, ambiente: Ambiente, contexto: str) -> str:
        """Executa o ciclo de decisão da IA."""
        self.auto_supervision(ambiente.recursos)
        resp = self.supervised(contexto)

        # Simula o resultado da ação (reforço)
        reward = 10 if "Ofensiva" in resp and random.random() > 0.6 else -5
        self.reinforcement(reward)

        return f"{self.nome} age como: {resp} (Evolução AI: {self.evolucao})"


class AIReparadora:
    def __init__(self, eficiencia=1.0):
        self.eficiencia = eficiencia

    def reparar(self, base: BaseMilitar):
        ganho = int(50 * self.eficiencia)
        base.energia.recarregar(ganho)
        logging.info(f"[IA REPARO] IA reparou {ganho} de energia na base {base.nome}.")
