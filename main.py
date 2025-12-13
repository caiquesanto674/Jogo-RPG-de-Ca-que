import logging
import random
from datetime import datetime

from nexus.componentes.base import BaseMilitar
from nexus.componentes.entidades import Arma, Guardiao, Inimigo, UnidadeCombate
from nexus.componentes.familia import MembroFamilia
from nexus.sistemas.ambiente import Ambiente
from nexus.sistemas.economia import Economia
from nexus.sistemas.ia import AI_NPC, AIReparadora
from nexus.sistemas.missoes import Missao
from nexus.sistemas.tecnologia import Tecnologia
from nexus.utils.log import LogGlobal

LOG_JOGO_FILE = "log_nexus_unificado.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler(LOG_JOGO_FILE)],
)


def regra_base_global():
    """Define a regra fundamental do universo do jogo."""
    return "Volição Ativa e Kernel 2.5"


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
        arma_base = Arma("Fusil Arcano", 90, "energia")
        unidade = UnidadeCombate(
            "Caíque (Protagonista)", "Comandante Mecha", armas=[arma_base], atk=100
        )
        self.base.unidades.append(unidade)

        # Inicialização de NPCs, Família e Ambiente
        self.ambientacao = [
            Ambiente("Vale Sombrio", "floresta"),
            Ambiente("Capital Arcanum", "cidade"),
        ]
        self.npc = AI_NPC("Ciel-Nexus", "normal")  # Sua IA de suporte
        self.familia = [MembroFamilia("Kael", "Liderança"), MembroFamilia("Lyna", "Estratégia")]
        self.ia_reparadora = AIReparadora()

    def ciclo_turno(self, contexto: str = "combate"):
        """Executa um único turno do jogo."""
        print(f"--- INÍCIO DO TURNO ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ---")

        # Módulos CORE
        self.economia.operar()
        self.tech.pesquisar(random.choice(["Criptografia Quântica", "Upgrade Cristalino"]))
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
            missao = Missao("Patrulha no Setor Gamma", dificuldade=random.randint(3, 7))
            missao.executar(self.base.unidades[0])

        # Relatório de Status
        print(f"\n✅ Status da Volição Ativa:")
        print(
            f"   Base: **{self.base.nome}** (Defesa: {self.base.defesa} / Nível Tech: {self.tech.nivel})"
        )
        print(
            f"   Protagonista ({self.base.unidades[0].nome}): Poder de Combate **{self.base.unidades[0].poder_combate()}**"
        )
        print(
            f"   Recursos (Ouro/Mana): **{self.economia.reservas['ouro']:.0f}** / **{self.economia.reservas['mana']}**"
        )
        print(f"   IA '{self.npc.nome}' - Evolução: **{self.npc.evolucao}** | Ação: *{acao_npc}*")
        print(f"   Ambiente: {self.ambientacao[0].nome} (Ciclo: {self.ambientacao[0].ciclo})")
        print("----------------------------------------------------------------")

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


def game_loop_principal():
    """Função principal de execução do jogo."""
    print(f"Iniciando Loop: {regra_base_global()}")
    motor = MotorJogo()

    # Simula 5 turnos com contextos variados
    contextos = ["combate", "crise", "exploracao", "diplomacia", "manutencao"]
    for i in range(1, 6):
        print(f"\n====================== TURNO {i} ======================")
        motor.ciclo_turno(contexto=random.choice(contextos))

    print("\n================== FIM DA SIMULAÇÃO ===================")
    print("Log de Eventos Chave:")
    for data, evento, args in motor.log.registros:
        print(f"[{data.strftime('%H:%M:%S')}] {evento}: {args}")


if __name__ == "__main__":
    game_loop_principal()
