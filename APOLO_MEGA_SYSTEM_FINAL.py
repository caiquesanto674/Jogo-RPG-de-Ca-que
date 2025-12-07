# APOLO_MEGA_SYSTEM_FINAL.py
# Versão Final Unificada: Jogo Híbrido (RPG/Tycoon) + Sistema de Correção Autônoma de IA
# Data: 07 Dezembro 2025

import random
import time
import hashlib
import re
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

# ===================== CONFIGURAÇÃO GLOBAL E UTILITÁRIOS =====================
CLASSES = ['Guerreiro', 'Mago', 'Comandante', 'Engenheiro', 'Assassino', 'Clérigo']
RACAS = ['Humano', 'Elfo', 'Orc', 'Demônio', 'Androide']
MAPA_TAMANHO = (30, 30)

def gerar_codigo_confirmacao(acao: str, cargo: str, nivel_tec: int) -> str:
    """Frases de Comportamento: Gera um hash de confirmação para comandos críticos."""
    raw = f"{acao}-{cargo}-{nivel_tec}:{datetime.now().microsecond}"
    return hashlib.sha256(raw.encode()).hexdigest()[:8].upper()

# ===================== AI CARDINAL — A DEUSA QUE NUNCA DEIXA VOCÊ PERDER =====================
class AICardinal:
    """
    Implementa a IA de suporte (Ciel Ascendido).
    Executa 'try-with-resources' divino para evitar o colapso do sistema.
    """
    def __init__(self):
        self.nome = "CIEL ASCENDIDO"
        self.correcoes = 0

    def salvar_realidade(self, protagonista: 'MonarcaAbsoluto', economia: 'Economia'):
        """Monitora e intervém (similar a um try-with-resources global) para evitar o colapso."""
        if (economia.reservas.get('comida', 0) < 500 or
            economia.reservas.get('mana', 0) < 300 or
            protagonista.moral < 20):

            print(f"\nAI CARDINAL: REALIDADE EM COLAPSO DETECTADA. INTERVENÇÃO DIVINA EXECUTADA.")
            economia.reservas['comida'] = max(3000, economia.reservas.get('comida', 0) + 5000)
            economia.reservas['mana'] = max(2000, economia.reservas.get('mana', 0) + 3000)
            protagonista.moral = 100.0
            self.correcoes += 1
            print(f"{self.nome} salvou o universo pela {self.correcoes}ª vez.")

# ===================== ECONOMIA & TECNOLOGIA (Tycoon + SSSS) =====================
class Economia:
    def __init__(self):
        self.reservas = {
            'ouro_conceitual': 30, 'materia_escura_ssss': 200, 'eter': 2000,
            'mana': 2500, 'comida': 3500, 'consciencia_remanescente': 20000
        }
        self.inflacao = 1.00

    def ciclo_ganho(self):
        """Simula o ganho passivo de recursos a cada ciclo."""
        self.reservas['ouro_conceitual'] = self.reservas.get('ouro_conceitual', 0) + 10
        self.reservas['comida'] = self.reservas.get('comida', 0) + 100
        # print("  [ECONOMIA] Ganhos do ciclo aplicados.")

class Tecnologia:
    def __init__(self):
        self.nivel = 1
        self.arvore = []

    def pesquisar(self, nome: str, custo: Dict[str, int], base_militar: 'BaseMilitar'):
        """Pesquisa tecnologia, gastando recursos complexos como Éter e SSSS."""
        if all(base_militar.recursos.get(res, 0) >= qtd for res, qtd in custo.items()):
            for res, qtd in custo.items():
                base_militar.recursos[res] -= qtd

            self.nivel += 1
            self.arvore.append(nome)
            print(f"🔬 Tec. pesquisada: {nome} | Nível {self.nivel}")
            return True
        return False

# ===================== ENTIDADES BASE, MONARCA E INIMIGO =====================
class Entidade:
    def __init__(self, nome: str, hp: int, pos: tuple):
        self.nome = nome
        self.hp = hp
        self.pos = pos
        self.energia = 100
        self.estado = 'neutro'
        self.inventario = []

class Personagem(Entidade):
    def __init__(self, nome, cargo='Jogador', raca=None, classe=None, base=None, pos=(0, 0)):
        super().__init__(nome, hp=120 if cargo == 'OWNER' else 100, pos=pos)
        self.raca = raca or random.choice(RACAS)
        self.classe = classe or random.choice(CLASSES)
        self.cargo = cargo
        self.base = base
        self.moral = 100.0 if cargo!='OWNER' else None # Moral só no Monarca
        self.humor = "neutro"

    def agir(self, acao: str, alvo: Optional[Entidade] = None):
        if acao == 'atacar' and alvo:
            dano = random.randint(15, 30)
            alvo.hp = max(0, alvo.hp - dano)
            return f"[{self.nome}] ataca {alvo.nome} e causa {dano} de dano! HP restante: {alvo.hp}"
        return f"{self.nome} executou ação: {acao}"

class MonarcaAbsoluto(Personagem):
    """Protagonista - Monarca Caíque (OWNER), com atributos de APOLO e Agony Overflow."""
    def __init__(self, nome: str, base: 'BaseMilitar'):
        super().__init__(nome, cargo="OWNER", raca="Humano", classe="Comandante", base=base)
        self.moral = 100.0
        self.indice_dimensional = 3.0
        self.harem = {"Luna": 100, "Calia Cardinal": 100, "Maria": 95}
        self.hp = 9999

    def ativar_volicao(self):
        """Mecânica Agony Overflow: A dor me torna mais forte (Evolução Reativa)."""
        if self.moral < 20:
            self.indice_dimensional += 0.5
            self.moral = 70
            print(f"\n⚡ AGONY OVERFLOW ATIVADO! NOVO ÍNDICE DIMENSIONAL: {self.indice_dimensional:.2f}")
            return True
        return False

class Inimigo(Personagem):
    """Inimigo de alto nível com Poder Psicológico e Sobrenatural."""
    def __init__(self, nome, cargo='Geral Inimigo', raca='Demônio', nivel_ameaca=65, poder_psicologico=True, pos=(0, 0)):
        super().__init__(nome, cargo, raca, classe='Mago', pos=pos)
        self.hp = 150
        self.nivel_forca = nivel_ameaca
        self.poder_psicologico = poder_psicologico

    def usar_poder(self, alvo: MonarcaAbsoluto):
        """Ataca a Moral do Monarca, mitigado pela defesa SSSS da Base."""
        if self.poder_psicologico and alvo.cargo == 'OWNER' and alvo.base:
            dano_base = self.nivel_forca * 0.75
            defesa_pct = alvo.base.defesa_psiquica
            dano_final = dano_base * (1.0 - defesa_pct)

            alvo.moral = max(0, alvo.moral - dano_final)
            alvo.humor = "dominado_psicologicamente"

            print(f"⚠️ [ATAQUE PSÍQUICO]: {self.nome} usou Manipulação Mental.")
            print(f"   Mitigação SSSS: {defesa_pct*100:.0f}% | Dano de Moral Recebido: {dano_final:.1f}")
            return 'PSICOLOGICO'
        return 'IDLE'

# ===================== BASE MILITAR (CORE NEXUS AURORA) =====================
class ComponenteBase:
    def __init__(self, nome: str, consumo_mana: int, producao_recurso: Optional[Dict[str, int]] = None):
        self.nome = nome
        self.consumo_mana = consumo_mana
        self.producao_recurso = producao_recurso if producao_recurso is not None else {}
        self.status = "OPERACIONAL"

class BaseMilitar:
    def __init__(self, nome, owner, economia, pos):
        self.nome = nome
        self.owner = owner
        self.economia = economia
        self.recursos = self.economia.reservas
        self.tecnologia = Tecnologia()
        self.defesa_psiquica = 0.0
        self.componentes: List[ComponenteBase] = []
        self._inicializar_componentes()

    def _inicializar_componentes(self):
        self.componentes.append(ComponenteBase("Reator de Éter Ω", 100, {'eter': 500, 'mana': 150}))
        self.componentes.append(ComponenteBase("Laboratório SSSS", 200, {'materia_escura_ssss': 50}))

    def ciclo_base(self):
        """CORREÇÃO DO BUG: Garante que a MANA seja tratada corretamente usando get/set seguro."""
        consumo_total_mana = sum(c.consumo_mana for c in self.componentes if c.status == "OPERACIONAL")
        producao_total = {}

        for comp in self.componentes:
            if comp.status == "OPERACIONAL":
                for recurso, quantidade in comp.producao_recurso.items():
                    producao_total[recurso] = producao_total.get(recurso, 0) + quantidade

        # FIX: Garante que 'mana' exista e atualiza o valor com segurança (Bug fixado)
        self.recursos['mana'] = self.recursos.get('mana', 0) - consumo_total_mana

        for recurso, quantidade in producao_total.items():
            self.recursos[recurso] = self.recursos.get(recurso, 0) + quantidade

        # print(f"  Consumo de MANA da Base: -{consumo_total_mana}")

    def aplicar_upgrade_psiquico(self):
        custo_ssss = 30
        if "Campo Psíquico SSSS" in self.tecnologia.arvore and self.recursos.get("materia_escura_ssss", 0) >= custo_ssss:
            self.recursos["materia_escura_ssss"] -= custo_ssss
            self.defesa_psiquica = 0.50
            print("🛡️ [UPGRADE ATIVO]: Campo de Estabilidade Psíquica SSSS ativado! (50% de mitigação)")
            return True
        return False

# ===================== AI NPC (INTELIGÊNCIA DE SUPORTE AVANÇADA) =====================
class AI_NPC_Suporte(Personagem):
    def tomar_decisao_suporte(self, monarca: MonarcaAbsoluto, inimigo: Inimigo):
        """Delibera ações baseadas no estado do Monarca (Suporte Tático Inteligente)."""

        if monarca.moral < 40 and monarca.base and monarca.base.defesa_psiquica < 0.5:
             # Prioridade 1: Ativar defesa se a moral estiver baixa e a defesa inativa
             print(f"[{self.nome} - SUPORTE TÁTICO]: Moral baixa. Iniciando ativação do Campo Psíquico SSSS.")
             monarca.base.aplicar_upgrade_psiquico()
             return 'ATIVAR_DEFESA_PSÍQUICA'

        if monarca.moral < 50 and self.classe in ('Clérigo', 'Mago'):
            # Prioridade 2: Restauração de Moral
            monarca.moral = min(100, monarca.moral + random.randint(10, 20))
            print(f"[{self.nome} - SUPORTE]: Usando Sinergia de Vontade. Moral restaurada.")
            return 'RESTAURAR_MORAL'

        if inimigo and inimigo.hp > 0:
            return self.agir('atacar', inimigo)

        return 'IDLE'

# ===================== MÓDULO DE GERENCIAMENTO DE CONFLITOS (NOVO) =====================

class CorrecaoLog:
    """Contabiliza e registra as ações do sistema de autocorreção (auto_correction_system.py)."""
    def __init__(self):
        self.total_conflitos_detectados = 0
        self.total_correcoes_aplicadas = 0
        self.log_registros: List[Dict[str, Any]] = []

    def registrar_conflito(self, arquivo: str, linhas: List[int]):
        self.total_conflitos_detectados += 1
        self.log_registros.append({"tipo": "CONFLITO_ARQUIVO", "arquivo": arquivo, "linhas_conflito": linhas, "status_correcao": "PENDENTE"})
        print(f"🚨 CONFLITO DETECTADO em {arquivo}.")

    def registrar_correcao(self, arquivo: str, decisao: str):
        self.total_correcoes_aplicadas += 1
        print(f"✅ [CORREÇÃO SUCESSO]: {arquivo} resolvido. Decisão: {decisao}")

    def relatorio_status(self):
        """Exibe um relatório das atividades de correção."""
        print(f"  [SISTEMA DE CORREÇÃO] Conflitos Detectados: {self.total_conflitos_detectados} | Correções Aplicadas: {self.total_correcoes_aplicadas}")

class ConflictResolver:
    """Simula a lógica da IA para detectar e resolver conflitos de código."""
    CONFLITO_PADRAO = re.compile(r'(<<<<<<<|========|>>>>>>>|\s*Accept incoming change\s*|\s*Accept current change\s*)')

    @staticmethod
    def simular_leitura_arquivo(conteudo_com_conflito: str) -> Tuple[bool, List[int]]:
        """Identifica se há marcadores de conflito no código (como no PR)."""
        em_conflito = any(ConflictResolver.CONFLITO_PADRAO.search(linha) for linha in conteudo_com_conflito.splitlines())
        return em_conflito, [] # Simplificado para simulação

    @staticmethod
    def resolver_conflito(conteudo_com_conflito: str, estrategia: str = "INCOMING") -> Tuple[str, str]:
        """Simula a resolução de um bloco de conflito (escolhe INCOMING = Feature da IA)."""
        if estrategia == "INCOMING":
             # Simula manter a lógica da nova feature/IA e descartar os marcadores de conflito
             resolvido = re.sub(r'<<<<<<<.*?========.*?>>>>>>>.*?', '', conteudo_com_conflito, flags=re.DOTALL)
             return resolvido, "INCOMING_IA_ASSISTIDA"
        return conteudo_com_conflito, "MANUAL"


# ===================== MOTOR FINAL — O CICLO UNIFICADO =====================
class Engine:
    def __init__(self):
        self.turno = 0
        self.economia = Economia()
        self.cardinal = AICardinal()
        self.base = BaseMilitar("CORE NEXUS AURORA", None, self.economia, (5, 5))
        self.protagonista = MonarcaAbsoluto("CAÍQUE APOLO Ω", self.base)
        self.base.owner = self.protagonista
        self.inimigos = [Inimigo("Lord Zarkon Ω", nivel_ameaca=90, poder_psicologico=True, pos=(10, 10))]
        self.aliados = [AI_NPC_Suporte("Calia Cardinal", "Clérigo", self.base)]
        self.log_manager = CorrecaoLog() # Sistema de organização de código/conflito

    def ciclo(self):
        self.turno += 1
        print(f"\n{'='*110}")
        print(f"                  CICLO {self.turno} — DOMÍNIO ABSOLUTO DO MONARCA CAÍQUE")

        # 1. Manutenção de Sistemas (Economia, Base, AI Cardinal)
        self.economia.ciclo_ganho()
        self.base.ciclo_base()
        self.cardinal.salvar_realidade(self.protagonista, self.economia)

        # 2. Ações do Protagonista (Poder)
        self.protagonista.ativar_volicao() # Agony Overflow (Evolução Reativa)

        # 3. Conflito (Combate Psicológico e Suporte)
        if self.inimigos:
            inimigo_atual = self.inimigos[0]

            # A. Ação do Inimigo (Ataque Psicológico)
            inimigo_atual.usar_poder(self.protagonista)

            # B. Ação do Aliado (Suporte Tático Inteligente)
            for aliado in self.aliados:
                aliado.tomar_decisao_suporte(self.protagonista, inimigo_atual)

            # C. Resposta do Protagonista
            self.protagonista.agir('atacar', inimigo_atual)

        # 4. Simulação de Gerenciamento de Conflito de Código
        if self.turno == 2:
            # Simula a ocorrência de um conflito em um arquivo de código
            conteudo_falso = "<<<<<<< HEAD \n Código Antigo \n ======= \n Código Novo da Feature \n >>>>>>> feature/nova-ia"

            if ConflictResolver.simular_leitura_arquivo(conteudo_falso)[0]:
                 self.log_manager.registrar_conflito("rpg_ai_feature.py", [1, 5])

                 # IA resolve o conflito automaticamente
                 _, decisao = ConflictResolver.resolver_conflito(conteudo_falso, "INCOMING")
                 self.log_manager.registrar_correcao("rpg_ai_feature.py", decisao)

                 print("\n🛠️ [IA CORREÇÃO ATIVADA]: Conflito de Código resolvido com sucesso pela IA de Assistência.")

        # 5. Relatório de Status
        print(f"\n--- STATUS CRÍTICO ---")
        print(f"  Moral: {self.protagonista.moral:.1f}/100 | Índice Dimensional: {self.protagonista.indice_dimensional:.2f}")
        print(f"  Defesa Psíquica SSSS: {self.base.defesa_psiquica * 100:.0f}% Ativa")
        self.log_manager.relatorio_status()
        print(f"{'='*110}")


# ============================= EXECUÇÃO FINAL & TESTE =============================
if __name__ == "__main__":
    print("\n" + "="*100)
    print("             INICIANDO APOLO MEGA SYSTEM FINAL (V2.0.1)")
    print("="*100)

    jogo = Engine()

    # Preparação: Pesquisa do campo Psíquico SSSS antes do combate
    custo_pesquisa = {"materia_escura_ssss": 50, "eter": 100}
    jogo.base.tecnologia.pesquisar("Campo Psíquico SSSS", custo_pesquisa, jogo.base)

    try:
        while jogo.turno < 4:
            jogo.ciclo()
            time.sleep(1.8)
    except KeyboardInterrupt:
        pass

    print("\n\nSIMULAÇÃO FINALIZADA. Domínio mantido.")
