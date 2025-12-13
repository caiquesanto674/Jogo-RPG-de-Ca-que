# === ARQUIVO PRINCIPAL DO NEXUS (Jogo RPG de Caíque) - UNIFICADO ===

import random
import uuid
import hashlib
import sys
import logging
import json
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
    "SUPORTE_SUCESSO": "Reforços e suporte enviados com sucesso!",
    "TECNOLOGIA_SUCESSO": "Melhoria tecnológica concluída com sucesso.",
    "TECNOLOGIA_FALHA": "Pesquisa falhou. Recursos insuficientes.",
    "EXPLORACAO_MUNDO": "Exploração de novo setor iniciada.",
    "GUARDIAO_DESPERTAR": "O Guardião despertou! Poder lendário ativado.",
    "BASE_RECRUTAR_SUCESSO": "Nova unidade recrutada e adicionada às suas forças.",
    "BASE_RECRUTAR_FALHA": "Falha no recrutamento. Verifique os recursos disponíveis.",
    "BASE_DEFESA_SUCESSO": "Defesas da base fortalecidas com sucesso.",
    "BASE_DEFESA_FALHA": "Melhoria das defesas falhou. Recursos insuficientes.",
    "ECONOMIA_FALHA_RECURSOS": "Alerta de escassez! A produção foi prejudicada.",
    "JOGO_SALVO_SUCESSO": "Progresso salvo com sucesso.",
    "JOGO_CARREGADO_SUCESSO": "Jogo carregado com sucesso.",
    "JOGO_CARREGADO_FALHA": "Falha ao carregar o jogo. O arquivo não foi encontrado ou está corrompido."
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

# --- MÓDULO DE ECONOMIA (TYCOON V3) ---
class Economia:
    """Gerencia reservas, produção, gastos e inflação dinâmica."""
    def __init__(self):
        self.reservas = {'ouro': 5000, 'aço': 3000, 'mana': 800, 'comida': 1500, 'energia': 900}
        self.producao_base = 2000
        self.inflacao = 1.0

    def operar(self):
        """Calcula a produção e atualiza a inflação."""
        producao_ajustada = int(self.producao_base * (2.0 - self.inflacao))
        if producao_ajustada < 0: producao_ajustada = 100

        for rec in self.reservas:
            self.reservas[rec] += int(producao_ajustada // len(self.reservas))

        self.inflacao *= (0.99 + random.random() * 0.03)
        logging.info(f"[ECONOMIA] Reservas atualizadas. Inflação: {self.inflacao:.2f}")

    def gastar_recursos(self, custos: Dict[str, int]) -> bool:
        """Verifica se há recursos suficientes e, em caso afirmativo, os deduz. Retorna True em caso de sucesso."""
        for recurso, valor in custos.items():
            if self.reservas.get(recurso, 0) < valor:
                logging.warning(f"[ECONOMIA] Falha ao gastar. Recurso insuficiente: {recurso}.")
                return False

        for recurso, valor in custos.items():
            self.reservas[recurso] -= valor

        logging.info(f"[ECONOMIA] Recursos gastos: {custos}")
        return True

# --- MÓDULO DE COMBATE (FORÇA BÉLICA V5) ---
class Arma:
    """Define as armas, seu poder de combate e tipo."""
    def __init__(self, nome: str, poder: int, tipo: str):
        self.nome, self.poder, self.tipo = nome, poder, tipo

    def to_dict(self):
        return {"nome": self.nome, "poder": self.poder, "tipo": self.tipo}

class UnidadeCombate:
    """Unidade militar com moral e arsenal."""
    def __init__(self, nome: str, classe: str, moral: int = 80, armas: List[Arma] = None, hp: int = 100, atk: int = 10, defn: int = 5, level: int = 1, exp: int = 0):
        self.nome, self.classe, self.moral = nome, classe, moral
        self.armas = armas if armas else []
        self.hp = hp
        self.atk = atk
        self.defn = defn
        self.level = level
        self.exp = exp

    def to_dict(self):
        return {
            "nome": self.nome, "classe": self.classe, "moral": self.moral,
            "hp": self.hp, "atk": self.atk, "defn": self.defn,
            "level": self.level, "exp": self.exp,
            "armas": [arma.to_dict() for arma in self.armas]
        }

    def poder_combate(self) -> int:
        """Calcula o poder total (ataque + armas)."""
        return self.atk + sum(a.poder for a in self.armas)

    def atacar(self, alvo: 'UnidadeCombate'):
        dano = max(1, self.atk - alvo.defn)
        alvo.hp -= dano
        logging.info(f"[COMBATE] {self.nome} causou {dano} de dano em {alvo.nome}.")
        return dano

    def ganhar_exp(self, valor):
        self.exp += valor
        if self.exp >= 100 * self.level:
            self.level += 1
            self.exp = 0
            self.atk += 2
            self.hp += 10
            logging.info(f"[PROMOÇÃO] {self.nome} avançou para o nível {self.level}!")

class Inimigo(UnidadeCombate):
    def __init__(self, nome, level):
        super().__init__(nome, "Inimigo", hp=50 + level*10, atk=5+level*2, defn=3+level)
        self.level = level

class Guardiao:
    """Representa uma entidade semi-divina com poderes sobrenaturais."""
    def __init__(self, nome: str, poder_unico: str):
        self.nome=nome; self.poder_unico=poder_unico; self.atento=False

    def despertar(self):
        """Ativa o poder único e lendário do Guardião."""
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
    """Gerencia a base militar, incluindo defesa, recrutamento e melhorias."""
    def __init__(self, nome: str, economia: Economia):
        self.nome = nome
        self.economia = economia
        self.nivel = 1
        self.defesa = 120
        self.unidades: List[UnidadeCombate] = []
        self.guardioes: List[Guardiao] = []
        self.energia = EnergiaBase(2000)

    def adicionar_guardiao(self, guardiao: Guardiao):
        self.guardioes.append(guardiao)

    def recrutar_unidade(self, nome: str, classe: str) -> Optional[UnidadeCombate]:
        """Tenta recrutar uma nova unidade, consumindo os recursos necessários."""
        custos = {'ouro': 150, 'aço': 50, 'comida': 20}
        if self.economia.gastar_recursos(custos):
            nova_unidade = UnidadeCombate(nome, classe)
            self.unidades.append(nova_unidade)
            logging.info(confirmar("BASE_RECRUTAR", True))
            return nova_unidade
        logging.warning(confirmar("BASE_RECRUTAR", False))
        return None

    def melhorar_defesa(self):
        """Tenta melhorar as defesas da base, consumindo os recursos necessários."""
        custo_melhoria = {'aço': 200 * self.nivel, 'energia': 100 * self.nivel}
        if self.economia.gastar_recursos(custo_melhoria):
            self.defesa += 50
            self.nivel += 1
            logging.info(confirmar("BASE_DEFESA", True) + f" (Nível: {self.nivel})")
        else:
            logging.warning(confirmar("BASE_DEFESA", False))

    def to_dict(self):
        return {
            "nome": self.nome, "nivel": self.nivel, "defesa": self.defesa,
            "unidades": [unidade.to_dict() for unidade in self.unidades]
        }

# --- MÓDULO DE TECNOLOGIA E HABILIDADES ---
class Tecnologia:
    """Gerencia a árvore de tecnologias, incluindo custos e pré-requisitos para pesquisa."""
    def __init__(self, economia: Economia):
        self.economia = economia
        self.tecnologias_desbloqueadas: List[str] = []
        self.arvore = {
            "Armamento Balístico": {'custo': {'aço': 150, 'ouro': 100}, 'prerequisito': None, 'buff': {'atk_unidade': 5}},
            "Medicina de Combate": {'custo': {'ouro': 120, 'comida': 80}, 'prerequisito': None, 'buff': {'hp_unidade': 20}},
            "Propulsão a Plasma": {'custo': {'energia': 300, 'mana': 150}, 'prerequisito': "Armamento Balístico", 'buff': {'poder_arma': 15}},
            "IA de Batalha": {'custo': {'ouro': 250, 'energia': 180}, 'prerequisito': "Propulsão a Plasma", 'buff': {'moral_unidade': 10}}
        }

    def pode_pesquisar(self, nome_tech: str) -> bool:
        """Verifica se uma tecnologia específica pode ser pesquisada, checando pré-requisitos."""
        if nome_tech in self.tecnologias_desbloqueadas:
            return False

        tech = self.arvore.get(nome_tech)
        if not tech:
            return False

        prerequisito = tech.get('prerequisito')
        if prerequisito and prerequisito not in self.tecnologias_desbloqueadas:
            return False

        return True

    def pesquisar(self, nome_tech: str):
        """Tenta pesquisar uma nova tecnologia, se todos os requisitos forem atendidos."""
        if not self.pode_pesquisar(nome_tech):
            logging.warning(f"[TECH] Não é possível pesquisar '{nome_tech}' no momento.")
            return

        custo = self.arvore[nome_tech]['custo']
        if self.economia.gastar_recursos(custo):
            self.tecnologias_desbloqueadas.append(nome_tech)
            # A lógica para aplicar o buff da tecnologia seria implementada aqui
            logging.info(f"[TECH] {confirmar('TECNOLOGIA', True)}: {nome_tech}")
        else:
            logging.warning(f"[TECH] {confirmar('TECNOLOGIA', False)} para '{nome_tech}'.")

# --- MÓDULOS AUXILIARES ---
class Ambiente:
    """Simula o ambiente do jogo, incluindo o ciclo de dia/noite e os recursos locais."""
    def __init__(self, nome: str, tipo: str, ciclo: str = "dia"):
        self.nome, self.tipo, self.ciclo = nome, tipo, ciclo
        self.recursos = {'agua': 1000, 'mana': 350, 'sombra': 0, 'lux': 120}

    def atualizar(self):
        """Alterna o ciclo entre dia e noite, ajustando os recursos do ambiente."""
        self.ciclo = 'noite' if self.ciclo == 'dia' else 'dia'
        if self.ciclo == 'noite':
            self.recursos['lux'] = max(0, self.recursos['lux']-90)
            self.recursos['sombra'] += 5
        else:
            self.recursos['lux'] += 90
            self.recursos['sombra'] = max(0, self.recursos['sombra']-2)

class LogGlobal:
    """Registra e armazena todos os eventos importantes que ocorrem no jogo."""
    def __init__(self): self.registros = []
    def registrar(self, evento: str, args: Any): self.registros.append((datetime.now(), evento, args))

class MembroFamilia:
    """Modela um membro de uma família, com foco em herança e talentos."""
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

    def executar(self, personagem: UnidadeCombate):
        chance = personagem.level * random.uniform(0.5, 1.5)
        if chance >= self.dificuldade:
            personagem.ganhar_exp(self.recompensa)
            logging.info(f"[MISSÃO] {personagem.nome} completou a missão '{self.nome}' com sucesso.")
            self.status = "concluída"
            return True
        else:
            personagem.hp -= 10
            logging.info(f"[MISSÃO] {personagem.nome} falhou na missão '{self.nome}'.")
            self.status = "falhou"
            return False

class AI_NPC:
    """Implementa uma IA de suporte adaptativa que evolui com o jogo."""
    def __init__(self, nome: str, comportamento: str = "normal"):
        self.nome, self.comportamento, self.evolucao = nome, comportamento, 0

    def auto_supervision(self, ambiente_recursos: Dict[str, int]):
        """Mecanismo de evolução ativa: a IA reage às mudanças no estado do mundo."""
        if ambiente_recursos.get('mana', 0) > 500:
            self.comportamento = "alerta estratégico"
            self.evolucao += 2

    def reinforcement(self, reward: int):
        """Mecanismo de evolução reativa: a IA aprende com o resultado de suas ações."""
        self.evolucao += reward

    def supervised(self, contexto: str) -> str:
        """Define a ação da IA com base no contexto atual do jogo."""
        if contexto == "combate": return "Ofensiva máxima (Foco: Alvos de maior ameaça)"
        elif contexto == "crise": return "Recuo Tático e Diplomacia de emergência"
        return "Patrulha padrão e coleta de dados"

    def agir(self, ambiente: Ambiente, contexto: str) -> str:
        """Executa o ciclo completo de tomada de decisão da IA."""
        self.auto_supervision(ambiente.recursos)
        resp = self.supervised(contexto)

        # Simula o resultado da ação para aprendizado por reforço
        reward = 10 if "Ofensiva" in resp and random.random() > 0.6 else -5
        self.reinforcement(reward)

        return f"{self.nome} age como: {resp} (Evolução AI: {self.evolucao})"

class AIReparadora:
    def __init__(self, eficiencia=1.0):
        self.eficiencia = eficiencia

    def reparar(self, base: BaseMilitar):
        ganho = int(50 * self.eficiencia)
        base.energia.recarregar(ganho)
        logging.info(f"[IA REPARO] A IA reparou {ganho} de energia na base {base.nome}.")

# ----------------------- SEÇÃO 3: LÓGICA PRINCIPAL (LOOP) -----------------------

class MotorJogo:
    """Motor principal do jogo, responsável por orquestrar os turnos e os sistemas."""
    def __init__(self):
        self.economia = Economia()
        self.tech = Tecnologia(self.economia)
        self.log = LogGlobal()

        # Inicialização da Base e Unidades
        self.base = BaseMilitar("Fortaleza Alpha Prime", self.economia)
        self.guardiao = Guardiao("Argus", "Vórtice Temporal")
        self.base.adicionar_guardiao(self.guardiao)
        arma_base = Arma("Fusil Arcano", 90, "Energia")
        unidade = UnidadeCombate("Caíque (Protagonista)", "Comandante Mecha", armas=[arma_base], atk=100)
        self.base.unidades.append(unidade)

        # Inicialização de NPCs, Família e Ambiente
        self.ambientacao = [Ambiente("Vale Sombrio", "Floresta"), Ambiente("Capital Arcanum", "Cidade")]
        self.npc = AI_NPC("Ciel-Nexus", "Padrão") # IA de suporte
        self.familia = [MembroFamilia("Kael", "Liderança"), MembroFamilia("Lyna", "Estratégia")]
        self.ia_reparadora = AIReparadora()

    def ciclo_turno(self, contexto: str = "combate"):
        """Executa todas as ações e lógicas de um único turno do jogo."""
        print(f"--- INÍCIO DO TURNO ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ---")

        # Módulos Centrais
        self.economia.operar()
        # Pesquisa tecnológica estratégica
        if self.tech.pode_pesquisar("Armamento Balístico"):
            self.tech.pesquisar("Armamento Balístico")
        elif self.tech.pode_pesquisar("Propulsão a Plasma"):
            self.tech.pesquisar("Propulsão a Plasma")
        elif self.tech.pode_pesquisar("IA de Batalha"):
            self.tech.pesquisar("IA de Batalha")

        for amb in self.ambientacao: amb.atualizar()

        # Ação da IA de Suporte
        acao_npc = self.npc.agir(self.ambientacao[0], contexto)
        self.log.registrar("AcaoNPC", acao_npc)
        self.ia_reparadora.reparar(self.base)

        # Ações da Base Militar (Recrutamento e Melhoria)
        if random.random() < 0.4: # 40% de chance de tentar recrutar
            self.base.recrutar_unidade(f"Soldado-{uuid.uuid4().hex[:4]}", "Infantaria")
        if random.random() < 0.2: # 20% de chance de tentar melhorar defesas
            self.base.melhorar_defesa()

        # Ação Militar e do Guardião
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
        print(f"\n✅ Relatório de Status da Volição Ativa:")
        print(f"   Base: **{self.base.nome}** (Defesa: {self.base.defesa} / Tecnologias: {len(self.tech.tecnologias_desbloqueadas)})")
        print(f"   Protagonista ({self.base.unidades[0].nome}): Poder de Combate **{self.base.unidades[0].poder_combate()}**")
        print(f"   Recursos (Ouro/Mana): **{self.economia.reservas['ouro']:.0f}** / **{self.economia.reservas['mana']}**")
        print(f"   IA '{self.npc.nome}' - Evolução: **{self.npc.evolucao}** | Ação: *{acao_npc}*")
        print(f"   Ambiente: {self.ambientacao[0].nome} (Ciclo: {self.ambientacao[0].ciclo})")
        print("----------------------------------------------------------------")

    def save_game(self, filename="save_game.json"):
        """Salva o estado atual do jogo em um arquivo no formato JSON."""
        estado_jogo = {
            "economia": self.economia.reservas,
            "tecnologia": self.tech.tecnologias_desbloqueadas,
            "base": self.base.to_dict()
        }
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(estado_jogo, f, indent=4, ensure_ascii=False)
        logging.info(confirmar("JOGO_SALVO", True))

    def load_game(self, filename="save_game.json"):
        """Carrega o estado do jogo a partir de um arquivo JSON."""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                estado_jogo = json.load(f)

            self.economia.reservas = estado_jogo["economia"]
            self.tech.tecnologias_desbloqueadas = estado_jogo["tecnologia"]

            base_data = estado_jogo["base"]
            self.base.nome = base_data["nome"]
            self.base.nivel = base_data["nivel"]
            self.base.defesa = base_data["defesa"]

            self.base.unidades = []
            for unidade_data in base_data["unidades"]:
                armas = [Arma(**arma_data) for arma_data in unidade_data["armas"]]
                unidade_data.pop("armas")
                self.base.unidades.append(UnidadeCombate(armas=armas, **unidade_data))

            logging.info(confirmar("JOGO_CARREGADO", True))
        except (FileNotFoundError, json.JSONDecodeError):
            logging.error(confirmar("JOGO_CARREGADO", False))

    def batalha(self):
        inimigo = Inimigo("Drone Rebelde", level=random.randint(1,5))
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
    """Função principal que inicializa e executa o loop do jogo."""
    print(f'Iniciando Simulação: {regra_base_global()}')
    motor = MotorJogo()
    motor.load_game()  # Tenta carregar um jogo salvo

    # Simula 5 turnos com contextos variados
    contextos = ["combate", "crise", "exploracao", "diplomacia", "manutencao"]
    for i in range(1, 6):
        print(f"\n====================== TURNO {i} ======================")
        motor.ciclo_turno(contexto=random.choice(contextos))

    motor.save_game() # Salva o jogo no final
    print("\n================== FIM DA SIMULAÇÃO ===================")
    print("Registro de Eventos-Chave:")
    for data, evento, args in motor.log.registros:
        print(f"[{data.strftime('%H:%M:%S')}] {evento}: {args}")

if __name__ == '__main__':
    game_loop_principal()

# === FIM DO ARQUIVO ===