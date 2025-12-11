# === ARQUIVO PRINCIPAL DO NEXUS (Jogo RPG de Caíque) - UNIFICADO ===

import random
import uuid
import hashlib
import sys
import logging
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Any, Optional

# =========================== CONFIGURAÇÃO E LOG ============================
LOG_JOGO_FILE = "log_nexus_unificado.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler(), logging.FileHandler(LOG_JOGO_FILE)]
)

# === ENUMERADORES E CÓDIGOS DE CONFIRMAÇÃO ===
class EstadoAto(Enum):
    OFENSIVO = 'OFENSIVO'
    DEFENSIVO = 'DEFENSIVO'
    DIPLOMACIA = 'DIPLOMACIA'
    SUPORTE = 'SUPORTE'
    EXPLORACAO = 'EXPLORACAO'

CODIGOS_CONFIRMACAO = {
    "MILITAR_SUCESSO": "Operação militar executada com êxito!",
    "MILITAR_FALHA": "Falha operacional. Perdas registradas.",
    "SUPORTE_SUCESSO": "Reforços e suporte enviados!",
    "TECNOLOGIA_SUCESSO": "Upgrade tecnológico ativado.",
    "EXPLORACAO_MUNDO": "Exploração iniciada.",
    "GUARDIAO_DESPERTAR": "Guardião despertado! Poder lendário ativo."
}
def confirmar(codigo: str, sucesso: bool = True) -> str:
    """Retorna a frase de confirmação formatada."""
    key = f"{codigo}_{'SUCESSO' if sucesso else 'FALHA'}"
    return CODIGOS_CONFIRMACAO.get(key, "Ação processada.")

# ----------------------- SEÇÃO 1: CORE E INICIALIZAÇÃO -----------------------
def regra_base_global():
    """Define a regra fundamental do universo do jogo."""
    return 'Volição Ativa e Kernel 2.5'

# ----------------------- SEÇÃO 2: MÓDULOS DE JOGO ------------------------

## MODULO: SISTEMA CARDINALIS - ECONOMIA E ANALISE
class GameController:
    """Gerencia recursos, taxas econômicas e realiza análises de confirmação de tecnologia."""

    def __init__(self, jogador):
        self.jogador = jogador
        self.recursos = {'Créditos': 10000, 'MinérioRaro': 50, 'TecPontos': 0}
        self.taxa_inflacao = 1.05
        self.nivel_tecnologico = 1.0 # Base para analise

    def AnaliseTecnologica(self, projeto_custo):
        """
        Analisa e confirma se a economia e a tecnologia suportam um novo projeto.
        Retorna True se aprovado e False se reprovado (economia fraca ou tecnlogia insuficiente).
        """
        # CÁLCULO DE VIABILIDADE: Nível Econômico vs. Custo
        viabilidade_eco = self.recursos['Créditos'] / projeto_custo

        # CÁLCULO DE VIABILIDADE: Tecnologia vs. Complexidade
        complexidade = projeto_custo / 5000

        if (viabilidade_eco > 0.5) and (self.nivel_tecnologico >= complexidade):
            # Aprovado
            self.recursos['Créditos'] -= projeto_custo
            self.recursos['TecPontos'] += int(projeto_custo / 1000)
            self.nivel_tecnologico += 0.1
            return True, "CONFIRMAÇÃO ECONÔMICA: Projeto Aprovado. Nível Tecnológico Atualizado."
        else:
            # Reprovado
            return False, f"ANÁLISE REPROVADA: Créditos ou Nível Tecnológico ({self.nivel_tecnologico:.2f}) insuficientes."

## MODULO: FORÇA BÉLICA E COMBATE
class UnidadeMilitar:
    """Representa qualquer unidade militar: Aliado, Inimigo, Mecha ou Tropa."""

    def __init__(self, nome, tipo, nivel_forca, poder_psicologico=None, custo_manutencao=0):
        self.nome = nome
        self.tipo = tipo # Ex: 'Tropa de Choque', 'Mecha Pesado', 'Inimigo Psíquico'
        self.nivel_base = nivel_forca
        self.poder_psicologico = poder_psicologico
        self.custo = custo_manutencao
        self.aliados_proximos = 0
        self.hp = 100 # Para compatibilidade com missões
        self.level = 1 # Para compatibilidade com missões

    def CalcularForcaBelica(self):
        """Calcula o Nível de Força Bélica (FB) total da unidade."""

        # FATOR 1: Nível Base e Tipo (Ex: Mechas têm bônus de Força)
        forca_tipo = self.nivel_base * (1.5 if 'Mecha' in self.tipo else 1.0)

        # FATOR 2: Bônus Psicológico/Habilidade (Profundidade e Detalhe)
        # O Poder Psicológico ('Comando', 'Aura', 'Previsão') adiciona Força Estratégica
        bônus_psico = 0
        if self.poder_psicologico == 'Comando':
            bônus_psico = 0.25 * self.aliados_proximos # Bônus de Comando aumenta com aliados

        # FATOR 3: Bônus de Aliança (Aliaods, conforme solicitado)
        bônus_alianca = self.aliados_proximos * 5

        forca_belica_total = forca_tipo + bônus_psico + bônus_alianca

        return forca_belica_total

    def ExibirPoder(self):
        """Exibe o detalhamento do poder da unidade, conforme preferência por profundidade."""
        print(f"\n--- DETALHE PROFUNDO - {self.nome} ({self.tipo}) ---")
        print(f"FORÇA BÉLICA TOTAL: {self.CalcularForcaBelica():.2f}")
        print(f"Nível Base: {self.nivel_base}")
        print(f"Poder Psicológico: {self.poder_psicologico if self.poder_psicologico else 'Nenhum'}")
        if self.poder_psicologico == 'Comando':
            print(f"Bônus de Comando (por {self.aliados_proximos} aliados): +{0.25 * self.aliados_proximos:.2f}")

class Guardiao:
    """Entidade semi-divina (Poderes Divinos/Sobrenaturais)."""
    def __init__(self, nome: str, poder_unico: str):
        self.nome=nome; self.poder_unico=poder_unico; self.atento=False

    def despertar(self):
        """Ativa o poder único do guardião."""
        if not self.atento:
            self.atento = True
            logging.info(confirmar("GUARDIAO", True))

class EnergiaBase:
    def __init__(self, energia_total=1000):
        self.energia_total = energia_total
        self.energia_atual = energia_total

    def consumir(self, valor):
        if valor <= self.energia_atual:
            self.energia_atual -= valor
            return True
        return False

    def recarregar(self, valor):
        self.energia_atual = min(self.energia_total, self.energia_atual + valor)

class BaseMilitar:
    """Base de Operações, Defesa e Recrutamento."""
    def __init__(self, nome: str):
        self.nome = nome
        self.nivel = 1
        self.defesa = 120
        self.unidades: List[UnidadeMilitar] = []
        self.guardioes: List[Guardiao] = []
        self.energia = EnergiaBase(2000)

    def adicionar_guardiao(self, guardiao: Guardiao):
        self.guardioes.append(guardiao)

# --- INTEGRADO DE: AI, Log e Família (AUXILIARES) ---
class LogGlobal:
    """Armazena todos os eventos importantes do jogo."""
    def __init__(self): self.registros = []
    def registrar(self, evento: str, args: Any): self.registros.append((datetime.now(), evento, args))

class MembroFamilia:
    """Sistema de Saga e Herança, gestão de herdeiros (Vida Escolar/Drama/Romance)."""
    def __init__(self, nome: str, talento: str):
        self.nome, self.talento = nome, talento
        self.herdeiros: List[MembroFamilia] = []
    def nova_geracao(self, herdeiro: 'MembroFamilia'): self.herdeiros.append(herdeiro)

class Missao:
    def __init__(self, nome, dificuldade):
        self.nome = nome
        self.dificuldade = dificuldade
        self.recompensa = dificuldade * 25
        self.status = "pendente"

    def executar(self, personagem: UnidadeMilitar):
        chance = personagem.level * random.uniform(0.5, 1.5)
        if chance >= self.dificuldade:
            logging.info(f"[MISSÃO] {personagem.nome} completou '{self.nome}'.")
            self.status = "concluída"
            return True
        else:
            personagem.hp -= 10
            logging.info(f"[MISSÃO] {personagem.nome} falhou em '{self.nome}'.")
            self.status = "falhou"
            return False

## MODULO: IA DE SUPORTE E COMPORTAMENTO (NPC Adaptativo)
class NPC_Comportamento:
    """Gerencia a IA adaptativa e as frases de comportamento."""

    def __init__(self, nome, faccao, sentimentos={'Confianca': 0.5, 'Medo': 0.2}):
        self.nome = nome
        self.faccao = faccao
        self.sentimentos = sentimentos

    def FraseComportamento(self, forca_do_jogador):
        """Gera uma frase de comportamento baseada na Força Bélica do jogador."""

        if forca_do_jogador > 200:
            # Medo e Submissão
            self.sentimentos['Medo'] = min(1.0, self.sentimentos['Medo'] + 0.1)
            return f"**[REATIVO] {self.nome} ({self.faccao}):** 'Nossa força não se compara. Recuar é a única estratégia sensata. Iniciando protocolo de rendição.'"

        elif forca_do_jogador > 100:
            # Respeito e Cautela
            self.sentimentos['Confianca'] = max(0, self.sentimentos['Confianca'] - 0.05)
            return f"**[ADAPTATIVO] {self.nome} ({self.faccao}):** 'O poder deles é notável. Devemos rever nossas táticas e buscar uma aliança econômica discreta.'"

        else:
            # Confiança e Desafio
            self.sentimentos['Confianca'] = min(1.0, self.sentimentos['Confianca'] + 0.1)
            return f"**[AGRESSIVO] {self.nome} ({self.faccao}):** 'Eles são fracos! O Sistema Cardinalis falhou! ATAQUEM com Força Bélica total!'"

class AIReparadora:
    def __init__(self, eficiencia=1.0):
        self.eficiencia = eficiencia

    def reparar(self, base: BaseMilitar):
        ganho = int(50 * self.eficiencia)
        base.energia.recarregar(ganho)
        logging.info(f"[IA REPARO] IA reparou {ganho} de energia na base {base.nome}.")


# ----------------------- SEÇÃO 3: LÓGICA PRINCIPAL (LOOP) -----------------------

class MotorJogo:
    """Motor principal que orquestra o ciclo de jogo (Turnos)."""
    def __init__(self):
        self.log = LogGlobal()

        # Inicialização da Força e Defesa
        self.base = BaseMilitar("Fortaleza Alpha Prime")
        self.guardiao = Guardiao("Argus", "Temporal Vortex")
        self.base.adicionar_guardiao(self.guardiao)
        unidade = UnidadeMilitar("Caíque (Protagonista)", "Mecha Pesado", 150, poder_psicologico='Comando')
        self.base.unidades.append(unidade)
        self.jogador = unidade # Definindo o jogador principal

        # Inicialização do GameController
        self.game_controller = GameController(self.jogador)

        # Inicialização de NPCs, Família e Ambiente
        self.npc = NPC_Comportamento("NexusAI", "Independente")
        self.familia = [MembroFamilia("Kael", "Liderança"), MembroFamilia("Lyna", "Estratégia")]
        self.ia_reparadora = AIReparadora()

    def ciclo_turno(self, contexto: str = "combate"):
        """Executa um único turno do jogo."""
        print(f"--- INÍCIO DO TURNO ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ---")

        # Módulos CORE
        sucesso, mensagem = self.game_controller.AnaliseTecnologica(random.randint(4000, 8000))
        logging.info(mensagem)


        # Ação da IA de Suporte
        acao_npc = self.npc.FraseComportamento(self.jogador.CalcularForcaBelica())
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
        print(f"   Base: **{self.base.nome}** (Defesa: {self.base.defesa} / Nível Tech: {self.game_controller.nivel_tecnologico:.2f})")
        self.jogador.ExibirPoder()
        print(f"   Recursos (Créditos/Minério Raro): **{self.game_controller.recursos['Créditos']:.0f}** / **{self.game_controller.recursos['MinérioRaro']}**")
        print(f"   IA '{self.npc.nome}': {acao_npc}")
        print("----------------------------------------------------------------")

    def batalha(self):
        inimigo = UnidadeMilitar("Drone Rebelde", "Inimigo", nivel_forca=random.randint(50, 250))
        self.log.registrar("BATALHA", f"Início da batalha contra {inimigo.nome}.")

        jogador = self.jogador
        forca_jogador = jogador.CalcularForcaBelica()
        forca_inimigo = inimigo.CalcularForcaBelica()

        if forca_jogador > forca_inimigo:
            vencedor = jogador
            self.log.registrar("BATALHA", f"Vencedor: {vencedor.nome} com Força Bélica {forca_jogador:.2f} contra {forca_inimigo:.2f}")
        else:
            vencedor = inimigo
            self.log.registrar("BATALHA", f"Vencedor: {vencedor.nome} com Força Bélica {forca_inimigo:.2f} contra {forca_jogador:.2f}")

        return vencedor

def game_loop_principal():
    """Função principal de execução do jogo."""
    print(f'Iniciando Loop: {regra_base_global()}')
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

if __name__ == '__main__':
    game_loop_principal()

# === FIM DO ARQUIVO ===