# nexus/sistemas/motor.py
import random
from datetime import datetime
import logging

# Importando todas as classes e funções necessárias dos novos módulos
from ..componentes.entidades import (
    BaseMilitar,
    Guardiao,
    Inimigo,
    MembroFamilia,
    UnidadeCombate,
)
from ..utils.helpers import LogGlobal, regra_base_global
from .ia import AI_NPC, AIReparadora
from .mecanicas_jogo import Ambiente, Economia, Missao
from .tecnologia import Tecnologia


class MotorJogo:
    """Motor principal que orquestra o ciclo de jogo (Turnos)."""

    def __init__(self):
        self.economia = Economia()
        self.tech = Tecnologia()
        self.log = LogGlobal()

        # Inicialização da Força e Defesa
        self.base = BaseMilitar("Fortaleza Alpha Prime")
        self.guardiao = Guardiao("Argus", "Temporal Vortex")
        self.base.adicionar_guardiao(self.guardiao)

        # A classe 'Arma' não é mais necessária com o novo sistema
        unidade = UnidadeCombate(
            "Caíque (Protagonista)",
            "Comandante Mecha",
            tech=self.tech,
            poder_psicologico="Comando",
        )
        self.base.unidades.append(unidade)

        # Inicialização de NPCs, Família e Ambiente
        self.ambientacao = [
            Ambiente("Vale Sombrio", "floresta"),
            Ambiente("Capital Arcanum", "cidade"),
        ]
        self.npc = AI_NPC("Ciel-Nexus", "normal")  # Sua IA de suporte
        self.familia = [
            MembroFamilia("Kael", "Liderança"),
            MembroFamilia("Lyna", "Estratégia"),
        ]
        self.ia_reparadora = AIReparadora()

    def ciclo_turno(self, contexto: str = "combate"):
        """Executa um único turno do jogo."""
        logging.info(f"--- INÍCIO DO TURNO ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ---")

        # Módulos CORE
        self.economia.operar()
        self.tech.pesquisar(
            random.choice(["Criptografia Quântica", "Upgrade Cristalino"])
        )
        for amb in self.ambientacao:
            amb.atualizar()

        # Ação da IA de Suporte
        acao_npc = self.npc.agir(self.ambientacao[0], contexto)
        self.log.registrar("AcaoNPC", acao_npc)
        self.ia_reparadora.reparar(self.base)

        # Ação Militar e Guardião
        if random.random() > 0.7:
            self.guardiao.despertar()
            self.log.registrar("Guardião", f"{self.guardiao.nome} ativado.")

        # Eventos Aleatórios
        if random.random() < 0.3:
            self.batalha()
        if random.random() < 0.2:
            missao = Missao(
                "Patrulha no Setor Gamma", dificuldade=random.randint(3, 7)
            )
            missao.executar(self.base.unidades[0])

        # Relatório de Status
        logging.info("\n✅ Status da Volição Ativa:")
        logging.info(f"   Base: **{self.base.nome}** (Defesa: {self.base.defesa} / Nível Tech: {self.tech.nivel})")
        logging.info(f"   Protagonista ({self.base.unidades[0].nome}): Força Bélica **{self.base.unidades[0].calcular_forca_belica():.2f}**")
        logging.info(f"   Recursos (Ouro/Mana): **{self.economia.reservas['ouro']:.0f}** / **{self.economia.reservas['mana']}**")
        logging.info(f"   IA '{self.npc.nome}' - Evolução: **{self.npc.evolucao}** | Ação: *{acao_npc}*")
        logging.info(f"   Ambiente: {self.ambientacao[0].nome} (Ciclo: {self.ambientacao[0].ciclo})")

    def batalha(self):
        inimigo = Inimigo("Drone Rebelde", level=random.randint(1, 5))
        self.log.registrar("BATALHA", f"Início da batalha contra {inimigo.nome}.")

        jogador = self.base.unidades[0]
        while inimigo.hp > 0 and jogador.hp > 0:
            jogador.atacar(inimigo)
            if inimigo.hp > 0:
                inimigo.atacar(jogador)

        vencedor = jogador if jogador.hp > 0 else inimigo
        self.log.registrar("BATALHA", f"Vencedor: {vencedor.nome}")
        return vencedor
