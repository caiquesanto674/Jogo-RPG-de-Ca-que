import logging
import random
from typing import Dict

from nexus.componentes.base import BaseMilitar
from nexus.sistemas.ambiente import Ambiente
from nexus.utils.personalidades_ia import PARAMETROS_PERSONALIDADE, PersonalidadeIA


class AI_NPC:
    """IA de suporte e narrativa com sistema de personalidade e falhas intencionais."""

    def __init__(self, nome: str, personalidade: PersonalidadeIA = PersonalidadeIA.PADRAO):
        self.nome = nome
        self.personalidade = personalidade
        self.parametros = PARAMETROS_PERSONALIDADE[personalidade]
        self.evolucao = 0

    def auto_supervision(self, ambiente_recursos: Dict[str, int]):
        """Evolução ativa: Reage ao estado do mundo."""
        if ambiente_recursos.get("mana", 0) > 500:
            self.comportamento = "alerta estratégico"
            self.evolucao += 2

    def reinforcement(self, reward: int):
        """Evolução reativa: Aprende com o sucesso/falha de suas ações."""
        self.evolucao += reward

    def _decidir_acao_base(self, contexto: str) -> str:
        """
        Decide a ação principal com base na personalidade e no contexto,
        mas ANTES da introdução de falhas intencionais.
        """
        acoes_possiveis = {
            "combate": ["Ataque Total", "Manobra Ofensiva", "Fintar Inimigo"],
            "crise": ["Recuo Estratégico", "Defesa Absoluta", "Pedido de Suporte"],
            "exploracao": ["Mapear Área", "Coletar Recursos", "Analisar Artefato"],
        }
        acoes_padrao = ["Patrulha Cautelosa", "Monitorar Sinais", "Coleta de Dados"]

        opcoes = acoes_possiveis.get(contexto, acoes_padrao)

        # A personalidade influencia a escolha
        if contexto == "combate":
            if random.random() < self.parametros["foco_ataque"] - 0.5:
                return "Ataque Total"
        elif contexto == "crise":
            if random.random() < self.parametros["foco_defesa"] - 0.5:
                return "Recuo Estratégico"

        return random.choice(opcoes)

    def agir(self, ambiente: Ambiente, contexto: str) -> str:
        """
        Executa o ciclo de decisão da IA, agora incorporando personalidade e falhas.
        """
        self.auto_supervision(ambiente.recursos)

        # 1. A IA decide a ação ideal com base em sua personalidade
        acao_ideal = self._decidir_acao_base(contexto)

        # 2. Introduzimos a "imperfeição perfeita"
        decisao_final = acao_ideal
        foi_erro = False
        if random.random() < self.parametros["chance_erro"]:
            foi_erro = True
            acoes_alternativas = [
                "Ação hesitante",
                "Erro de cálculo tático",
                "Foco no alvo errado",
                "Avanço precipitado",
            ]
            decisao_final = random.choice(acoes_alternativas)

        # 3. Reforço e feedback
        # O reforço agora depende se a ação foi bem-sucedida, não apenas da ação em si
        sucesso_da_acao = random.random() > 0.4  # Simulação simples de sucesso
        reward = 10 if sucesso_da_acao and not foi_erro else -10
        self.reinforcement(reward)

        # 4. Construção do log de output
        desc_personalidade = self.parametros["descricao"]
        output = (
            f"IA {self.nome} ({desc_personalidade}) | "
            f"Ação Ideal: '{acao_ideal}' -> Decisão Final: '{decisao_final}'"
        )
        if foi_erro:
            output += " (Falha Intencional!)"

        return output


class AIReparadora:
    def __init__(self, eficiencia=1.0):
        self.eficiencia = eficiencia

    def reparar(self, base: BaseMilitar):
        ganho = int(50 * self.eficiencia)
        base.energia.recarregar(ganho)
        logging.info(f"[IA REPARO] IA reparou {ganho} de energia na base {base.nome}.")
