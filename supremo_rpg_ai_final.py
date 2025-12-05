import random
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from enum import Enum

# =================== SETUPS GLOBAIS E CÓDIGOS DE CONFIRMAÇÃO ===================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler(), logging.FileHandler("universo_jogo.log")]
)

class EstadoAto(Enum):
    OFENSIVO = 'OFENSIVO'
    DEFENSIVO = 'DEFENSIVO'
    DIPLOMACIA = 'DIPLOMACIA'
    SUPORTE = 'SUPORTE'
    EXPLORACAO = 'EXPLORACAO'

FRASES_CONFIRMACAO = {
    "MILITAR_SUCESSO": "Missão militar concluída com sucesso!",
    "MILITAR_FALHA": "Falha operacional. Recuo forçado.",
    "TECNOLOGIA_SUCESSO": "Nova tecnologia desbloqueada.",
    "EXPLORACAO_SUCESSO": "Exploração expandiu o mapa.",
    "GUARDIAO_DESPERTAR": "Guardião desperto! Poder ativado."
}
def confirmar(acao, sucesso=True):
    k = f"{acao}_{'SUCESSO' if sucesso else 'FALHA'}"
    return FRASES_CONFIRMACAO.get(k, "Ação processada.")

# =================== SISTEMA ECONÔMICO ===================
class Economia:
    def __init__(self):
        self.reservas = {'ouro': 4500, 'aço': 2800, 'energia': 1200, 'mana': 700, 'alimentos': 1800}
        self.producao = 1800
        self.inflacao = 1.0
    def operar(self):
        for k in self.reservas:
            self.reservas[k] += self.producao // len(self.reservas)
        self.inflacao *= (0.98 + random.random() * 0.02)
        logging.info("[ECONOMIA] Reservas e inflação atualizadas.")

# =================== SISTEMA TECNOLÓGICO ===================
class Tecnologia:
    def __init__(self):
        self.nivel = 1
        self.buffs = []
        self.pesquisas = []
    def pesquisar(self, tema):
        self.nivel += 1
        self.pesquisas.append(tema)
        logging.info(confirmar("TECNOLOGIA", True))

# =================== AMBIENTE DINÂMICO ===================
class Ambiente:
    def __init__(self, nome, tipo, ciclo="dia"):
        self.nome, self.tipo, self.ciclo = nome, tipo, ciclo
        self.recursos = {'agua': 950, 'mana': 300, 'sombra': 5, 'lux': 110}
        self.entidades: List[Any] = []
    def atualizar(self):
        self.ciclo = 'noite' if self.ciclo == 'dia' else 'dia'
        if self.ciclo == 'noite':
            self.recursos['lux'] = max(0, self.recursos['lux'] - 85)
            self.recursos['sombra'] += 8
        else:
            self.recursos['lux'] += 85
            self.recursos['sombra'] = max(0, self.recursos['sombra'] - 4)

# ===================== VEÍCULO E MONTARIA =====================
class Veiculo:
    def __init__(self, tipo, velocidade, capacidade):
        self.tipo, self.velocidade, self.capacidade = tipo, velocidade, capacidade
class Montaria:
    def __init__(self, nome, tipo, bonus, moral=100):
        self.nome, self.tipo, self.bonus, self.moral = nome, tipo, bonus, moral

# =================== ARSENAL E UNIDADES DE COMBATE ===================
class Arma:
    def __init__(self, nome, poder, tipo):
        self.nome, self.poder, self.tipo = nome, poder, tipo

class Unidade:
    def __init__(self, nome, classe, forca, moral=85, armas=None):
        self.nome, self.classe, self.forca, self.moral = nome, classe, forca, moral
        self.armas = armas if armas else []
    def poder_combate(self):
        return self.forca + sum(a.poder for a in self.armas)

class Guardiao:
    def __init__(self, nome, poder_unico):
        self.nome, self.poder_unico, self.atento = nome, poder_unico, False
    def despertar(self):
        if not self.atento:
            self.atento = True
            logging.info(confirmar("GUARDIAO_DESPERTAR", True))

class BaseMilitar:
    def __init__(self, nome):
        self.nome, self.nivel = nome, 1
        self.recursos = {'aço': 1000, 'mana': 400, 'pop': 150}
        self.defesa = 110
        self.unidades: List[Unidade] = []
        self.guardioes: List[Guardiao] = []
    def add_guardiao(self, guardiao): self.guardioes.append(guardiao)
    def evoluir(self):
        if self.recursos['aço'] >= 900:
            self.nivel += 1
            self.recursos['aço'] -= 900
            self.defesa += 20
            logging.info(confirmar("MILITAR", True))
            return True
        logging.warning(confirmar("MILITAR", False))
        return False

# =================== FAMÍLIA, SAGA E LOG ===================
class MembroFamilia:
    def __init__(self, nome, talento):
        self.nome, self.talento, self.herdeiros = nome, talento, []
    def nova_geracao(self, filho): self.herdeiros.append(filho)

class LogGlobal:
    def __init__(self): self.linhas = []
    def registrar(self, evento, args): self.linhas.append((datetime.now(), evento, args))

# =================== IA MULTINÍVEL DO NPC ===================
class NPC_AI:
    def __init__(self, nome, perfil="neutro"):
        self.nome, self.perfil, self.evolucao = nome, perfil, 0
    def auto_supervisao(self, ambiente_recursos):
        if ambiente_recursos['mana'] > 300:
            self.perfil = "atento"
            self.evolucao += 1
    def reforco(self, recompensa):
        self.evolucao += 1 if recompensa > 0 else -1
    def supervisionado(self, contexto):
        if contexto == "combate": return "Ofensivo total"
        if contexto == "crise": return "Recuo/Estratégico"
        return "Patrulha básica"
    def agir(self, ambiente, contexto):
        self.auto_supervisao(ambiente.recursos)
        resp = self.supervisionado(contexto)
        recomp = 10 if resp == "Ofensivo total" else -4
        self.reforco(recomp)
        return f"{self.nome} age em: {resp} [nv AI={self.evolucao}]"

# =================== SISTEMA DE MISSÕES ===================
class Missao:
    def __init__(self, descricao, dificuldade):
        self.descricao, self.dificuldade, self.status = descricao, dificuldade, "pendente"
    def concluir(self):
        self.status = "concluída"
        logging.info(f"Missão '{self.descricao}' concluída.")

# =================== MOTOR UNIFICADO E LOOP PRINCIPAL ===================
class MotorJogo:
    def __init__(self):
        self.economia = Economia()
        self.tech = Tecnologia()
        self.log = LogGlobal()
        self.base = BaseMilitar("Fortaleza Alfa")
        self.ambientes = [Ambiente("Cidade Aurora", "cidade"), Ambiente("Floresta Antiga", "floresta")]
        self.npc = NPC_AI("Ardor")
        self.guardiao = Guardiao("Argus", "Temporal Vortex")
        self.base.add_guardiao(self.guardiao)
        unidade = Unidade("Legião do Crepúsculo", "Soldado de Elite", 75, armas=[Arma("Lâmina de Éter", 95, "energia")])
        self.base.unidades.append(unidade)
        self.familia = [MembroFamilia("Kael", "Liderança")]
        self.missoes = [Missao("Defender a Cidade Aurora", 3), Missao("Explorar a Floresta Antiga", 2)]
        # Recursos não utilizados no loop, mas disponíveis para expansão
        self.veiculo = Veiculo("Transporte Blindado", 80, 10)
        self.montaria = Montaria("Grifo Imperial", "Aérea", "Bônus de Moral")

    def ciclo_turno(self, contexto="combate"):
        self.economia.operar()
        self.tech.pesquisar("Criptografia Quântica")
        for amb in self.ambientes: amb.atualizar()
        acao_npc = self.npc.agir(self.ambientes[0], contexto)
        self.log.registrar("NPC", acao_npc)
        for mis in self.missoes:
            if mis.status == "pendente" and random.random() > 0.6:
                mis.concluir()
        self.guardiao.despertar()

        # --- SAÍDA DO CONSOLE ---
        print(f"\n⚔️  Base {self.base.nome} | Defesa: {self.base.defesa} | Unidades: {len(self.base.unidades)}")
        print(f"🌳  Ambientes: {[a.nome for a in self.ambientes]} | Ciclo: {[a.ciclo for a in self.ambientes]}")
        print(f"🤖  NPC(AI): {acao_npc}")
        print(f"⭐  Família: {[fm.nome for fm in self.familia]}")
        print(f"🗺️  Missões: [{'; '.join([m.descricao + ':' + m.status for m in self.missoes])}]")
        print(f"🛡️  Guardião: {self.guardiao.nome} ativo={self.guardiao.atento}\n")

# =================== EXECUÇÃO ===================
def main():
    """ Função principal que executa a simulação do jogo. """
    engine = MotorJogo()
    for i in range(3):
        print(f"== TURNO {i+1} ==")
        engine.ciclo_turno(contexto=random.choice(["combate", "crise", "exploracao"]))
    print("\nLOG FINAL DO JOGO:")
    for e in engine.log.linhas:
        print(e)

if __name__ == "__main__":
    main()
