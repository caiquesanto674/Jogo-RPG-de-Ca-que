import random
import uuid
import hashlib
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Any, Optional

# =================== LOG GLOBAL/CONFIRMAÇÃO ===================
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler(), logging.FileHandler("jogo_master.log")]
)

CODIGOS_CONFIRMACAO = {
    "MILITAR_SUCESSO": "Operação militar executada com êxito!",
    "MILITAR_FALHA": "Falha operacional. Perdas registradas.",
    "TECNOLOGIA_SUCESSO": "Upgrade tecnológico ativado.",
    "EXPLORACAO_MUNDO": "Exploração iniciada.",
    "GUARDIAO_DESPERTAR": "Guardião despertado! Poder lendário ativo."
}
def frase_confirmacao(codigo, sucesso=True):
    key = f"{codigo}_{'SUCESSO' if sucesso else 'FALHA'}"
    return CODIGOS_CONFIRMACAO.get(key, "Ação processada.")

# =================== ENUM DE COMPORTAMENTO ===================
class EstadoComportamento(Enum):
    OFENSIVO = 'OFENSIVO'
    DEFENSIVO = 'DEFENSIVO'
    RECUO = 'RECUO'
    MAGIA = 'MAGIA'
    MANUTENCAO = 'MANUTENCAO'
    EXPLORACAO = 'EXPLORACAO'

# =================== CLASSE ECONOMIA/TYCOON ===================
class Economia:
    def __init__(self):
        self.reservas = {'ouro': 5000, 'aço': 3000, 'mana': 800, 'comida': 1500, 'energia': 900}
        self.producao = 2000
        self.inflacao = 1.0
    def operar(self):
        for rec in self.reservas:
            self.reservas[rec] += int(self.producao // len(self.reservas))
        self.inflacao *= (0.99 + random.random() * 0.02)
        logging.info("[ECONOMIA] Reservas e produção atualizadas.")

# =================== TECNOLOGIA E UPGRADE ===================
class Tecnologia:
    def __init__(self):
        self.nivel = 1
        self.buffs = []
        self.descobertas = []
    def pesquisar(self, tema):
        self.nivel += 1
        self.descobertas.append(tema)
        logging.info(f"[TECH] Nova pesquisa: {tema} (nível {self.nivel})")

# =================== RECURSO/ITEM ===================
class Recurso:
    def __init__(self, nome, valor_base):
        self.nome, self.valor_base, self.quantidade = nome, valor_base, 0

# =================== AMBIENTE/DIA/NOITE/SOMBRA ===================
class Ambiente:
    def __init__(self, nome, tipo, ciclo="dia"):
        self.nome, self.tipo, self.ciclo = nome, tipo, ciclo
        self.recursos = {'agua': 1000, 'mana': 350, 'sombra': 0, 'lux': 120}
        self.entidades: List['AgenteBase'] = []
    def atualizar(self):
        self.ciclo = 'noite' if self.ciclo == 'dia' else 'dia'
        if self.ciclo == 'noite':
            self.recursos['lux'] = max(0, self.recursos['lux']-90)
            self.recursos['sombra'] += 2
        else:
            self.recursos['lux'] += 90
            self.recursos['sombra'] = max(0, self.recursos['sombra']-1)

# =================== VEÍCULO / MONTARIA ===================
class Veiculo:
    def __init__(self, tipo, velocidade, capacidade):
        self.tipo = tipo; self.velocidade = velocidade; self.capacidade = capacidade
class Montaria:
    def __init__(self, nome, tipo, bonus, moral=100):
        self.nome = nome; self.tipo = tipo; self.bonus = bonus; self.moral = moral

# =================== BASE MILITAR, GUARDIÃO, ARMAS, UNIDADE ===================
class BaseMilitar:
    def __init__(self, nome):
        self.nome = nome
        self.nivel = 1
        self.recursos = {'aço': 1000, 'mana': 300, 'populacao': 200}
        self.defesa = 120
        self.unidades = []
        self.guardioes = []
    def adicionar_guardiao(self, guardiao):
        self.guardioes.append(guardiao)

class Arma:
    def __init__(self, nome, poder, tipo):
        self.nome, self.poder, self.tipo = nome, poder, tipo

class UnidadeCombate:
    def __init__(self, nome, classe, forca, moral=80, armas=None):
        self.nome, self.classe, self.forca, self.moral = nome, classe, forca, moral
        self.armas = armas if armas else []
    def poder_combate(self):
        return self.forca + sum(a.poder for a in self.armas)

# =================== LOG E FAMÍLIA SAGA ===================
class LogGlobal:
    def __init__(self): self.registros = []
    def registrar(self, evento, args): self.registros.append((datetime.now(), evento, args))

class MembroFamilia:
    def __init__(self, nome, talento):
        self.nome, self.talento = nome, talento
        self.herdeiros = []
    def nova_geracao(self, herdeiro): self.herdeiros.append(herdeiro)

# =================== AI: AUTO-SUPERVISÃO, REFORÇO, SUPERVISIONADO ===================
class AI_NPC:
    def __init__(self, nome, comportamento="normal"):
        self.nome, self.comportamento, self.evolucao = nome, comportamento, 0
    def auto_supervision(self, ambiente):
        if ambiente['mana'] > 500:
            self.comportamento = "alerta"
            self.evolucao += 2
    def reinforcement(self, acao, reward):
        if reward > 0: self.evolucao += 1
        else: self.evolucao -= 1
    def supervised(self, contexto):
        if contexto == "combate": return "Ofensiva máxima"
        elif contexto == "crise": return "Recuar/Diplomacia"
        return "Ação padrão"
    def agir(self, ambiente, contexto):
        self.auto_supervision(ambiente.recursos)
        resp = self.supervised(contexto)
        reward = 10 if resp == "Ofensiva máxima" else -5
        self.reinforcement(resp, reward)
        return f"{self.nome} age como: {resp} (evolução: {self.evolucao})"

# =================== NUCLEO DO JOGO E CICLO ===================
class MotorJogo:
    def __init__(self):
        self.economia = Economia()
        self.tech = Tecnologia()
        self.log = LogGlobal()
        self.base = BaseMilitar("Arcanum Prime")
        self.ambientacao = [Ambiente("Vale Sombrio", "floresta"), Ambiente("Fortaleza Selvagem", "cidade")]
        self.npc = AI_NPC("NexusGuard", "normal")
        self.arma_base = Arma("Fusil Arcano", 90, "energia")
        self.unidade = UnidadeCombate("Escudeiro", "Soldado", 65, armas=[self.arma_base])
        self.base.unidades.append(self.unidade)
        self.base.adicionar_guardiao("Argus the Everwatch")
    def ciclo_turno(self, contexto="combate"):
        self.economia.operar()
        self.tech.pesquisar("Upgrade Cristalino")
        for amb in self.ambientacao: amb.atualizar()
        acao_npc = self.npc.agir(self.ambientacao[0], contexto)
        self.log.registrar("AcaoNPC", acao_npc)
        print(f"Base: {self.base.nome} | Defesa: {self.base.defesa}")
        print(f"Unidade: {self.unidade.nome} poder={self.unidade.poder_combate()} | Arma: {self.arma_base.nome}")
        print(f"NPC: {acao_npc}")

# =================== EXECUÇÃO ===================
if __name__ == "__main__":
    engine = MotorJogo()
    for i in range(3):
        print(f"\n==== Ciclo {i+1}: ====")
        engine.ciclo_turno(contexto=random.choice(["combate", "crise", "exploracao"]))
    print("\nResumo de LOG:")
    for reg in engine.log.registros:
        print(reg)