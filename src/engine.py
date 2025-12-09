# src/engine.py

import random
import time
from src.core.monarca import MonarcaAbsoluto
from src.core.cardinal import AICardinal
from src.systems.economia import EconomiaUnificada
from src.systems.tecnologia import Tecnologia
from src.systems.base_militar import BaseMilitarUnificada
from src.systems.unidades import UnidadeMilitar
from src.systems.ai_npc import AI_NPC
from src.events.quiz import EventoQuiz
from src.events.mundo import MundoSimulado
from src.utils.log_protocol import LogSistema, ProtocoloConfirmacao

class JogoFinalMonarca:
    def __init__(self, nome_monarca: str):
        self.log = LogSistema()
        self.protagonista = MonarcaAbsoluto(nome_monarca)
        self.economia = EconomiaUnificada()
        self.tecnologia = Tecnologia()
        self.cardinal = AICardinal()
        self.base_militar = BaseMilitarUnificada(self.protagonista, self.economia, self.tecnologia)
        self.mundo_simulado = MundoSimulado(self.log)
        self.evento_quiz = EventoQuiz(self.protagonista, self.log)
        self.npc = AI_NPC("LEGEON", "analítico", 3, self.tecnologia)
        self.turno = 0
        self._inicializar_elementos()

    def _inicializar_elementos(self):
        unidade_inicial = UnidadeMilitar("Guardião do Nexus", "tanque", 120, tech=self.tecnologia, poder_psicologico='Comando', aliados_proximos=2)
        self.base_militar.unidades.append(unidade_inicial)
        self.log.registrar("SISTEMA", "Engine", "Jogo inicializado com sucesso.")

    def ciclo(self):
        self.turno += 1
        self.log.registrar("TURNO", "Engine", f"Iniciando Ciclo {self.turno}")

        # --- FASE DE SIMULAÇÃO DE FUNDO ---
        self.economia.ciclo()
        self.mundo_simulado.simular_turno()
        self.cardinal.salvar_realidade(self)

        # --- FASE DE AÇÕES DO JOGADOR (MONARCA) ---
        if self.turno % 2 != 0: self.protagonista.ativar_volicao()
        if self.turno % 3 == 0: self.protagonista.sinergia_harem()
        if self.turno % 4 == 0: self.tecnologia.pesquisar(random.choice(['IA', 'Plasma']))

        # --- FASE DE EVENTOS ---
        if self.turno % 5 == 0:
            self.evento_quiz.iniciar()

        # --- FASE DE IA E MILITAR ---
        forca_total_monarca = sum(u.poder_combate() for u in self.base_militar.unidades)
        acao_npc = self.npc.agir(forca_total_monarca, self.log)

        if acao_npc == 'atacar':
            self.base_militar.expandir(5000)
            for u in self.base_militar.unidades: u.moral = max(50, u.moral - 5)

        codigo_conf = ProtocoloConfirmacao.gerar(acao_npc, self.npc.nome, self.npc.nivel)
        self.log.registrar("PROTOCOLO", "Confirmação", f"Ação '{acao_npc}' confirmada com código {codigo_conf[:12]}...")

        # --- FASE DE RELATÓRIO ---
        print("\n--- RELATÓRIO DO TURNO ---")
        print(f"  Monarca: {self.protagonista.nome} | Patente: {self.protagonista.patente} | Moral: {self.protagonista.moral:.1f}")
        print(f"  Créditos: {self.economia.reservas['creditos']} | Matéria Escura: {self.economia.reservas['materia_escura_ssss']}")
        print(f"  Nível da Base: {self.base_militar.nivel} | Poder de Combate Total: {forca_total_monarca:.2f}")
        print("---------------------------\n")
