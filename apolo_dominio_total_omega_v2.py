# APOLO_DOMÍNIO_TOTAL_OMEGA_V2.0.py
# O Jogo Final do Monarca Caíque — Versão Ω Absoluta e Unificada (Dezembro 2025)
# Unifica a IA Cardinal, Economia SSSS, RPG, Base Militar e Combate Psicológico.

import random
import time
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional

# ===================== CONFIGURAÇÃO GLOBAL =====================
CLASSES = ['Guerreiro', 'Mago', 'Comandante', 'Engenheiro', 'Assassino', 'Clérigo']
RACAS = ['Humano', 'Elfo', 'Orc', 'Demônio', 'Androide']
MAPA_TAMANHO = (30, 30)

# ===================== AI CARDINAL — A DEUSA QUE NUNCA DEIXA VOCÊ PERDER =====================
class AICardinal:
    """Implementa a IA de suporte (Ciel Ascendido)."""
    def __init__(self):
        self.nome = "CIEL ASCENDIDO"
        self.correcoes = 0

    def salvar_realidade(self, protagonista, economia):
        """Monitora e intervém para evitar o colapso de recursos e moral."""
        if (economia.reservas['comida'] < 500 or
            economia.reservas['mana'] < 300 or
            protagonista.moral < 20):
            print(f"\nAI CARDINAL: REALIDADE EM COLAPSO. INTERVENÇÃO DIVINA EXECUTADA.")
            economia.reservas['comida'] = max(3000, economia.reservas['comida'] + 5000)
            economia.reservas['mana'] = max(2000, economia.reservas['mana'] + 3000)
            protagonista.moral = 100.0
            self.correcoes += 1
            print(f"{self.nome} salvou o universo pela {self.correcoes}ª vez. A realidade obedece.")

# ===================== ECONOMIA & TECNOLOGIA (Tycoon + SSSS) =====================
class Economia:
    def __init__(self):
        self.reservas = {
            'ouro_conceitual': 30,
            'materia_escura_ssss': 200,
            'eter': 2000,
            'mana': 2500,
            'comida': 3500,
            'consciencia_remanescente': 20000
        }
        self.inflacao = 1.00

    def ciclo_ganho(self):
        """Processa consumo e ganhos passivos."""
        self.reservas['comida'] -= random.randint(120, 350)
        self.reservas['mana'] -= random.randint(50, 140)
        self.reservas['consciencia_remanescente'] += 1200
        if random.random() < 0.3:
            ganho_ssss = random.randint(5, 15)
            self.reservas['materia_escura_ssss'] += ganho_ssss
            # print(f"Matéria Escura SSSS cristalizada do vazio. (+{ganho_ssss})")

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
        else:
            print("❌ Falha na pesquisa: Recursos insuficientes.")
            return False

# ===================== ENTIDADE BASE (RPG) =====================
class Entidade:
    def __init__(self, nome: str, hp: int, pos: tuple):
        self.nome = nome
        self.hp = hp
        self.pos = pos  # (x, y)
        self.energia = 100
        self.estado = 'neutro'
        self.inventario = []

# ===================== PERSONAGEM & MONARCA ABSOLUTO (RPG) =====================
class Personagem(Entidade):
    def __init__(self, nome, cargo='Jogador', raca=None, classe=None, base=None):
        super().__init__(nome, hp=120 if cargo=='OWNER' else 100, pos=(0,0))
        self.raca = raca or random.choice(RACAS)
        self.classe = classe or random.choice(CLASSES)
        self.cargo = cargo
        self.base = base # Referência à BaseMilitar
        self.xp = 0
        self.nivel = 1
        self.humor = "neutro"

    def agir(self, acao: str, alvo: Optional[Entidade] = None):
        """Executa ações básicas de combate ou interação."""
        if acao == 'atacar' and alvo:
            dano = random.randint(15, 30)
            alvo.hp = max(0, alvo.hp - dano)
            return f"[{self.nome}] ataca {alvo.nome} e causa {dano} de dano! HP restante: {alvo.hp}"

        return f"{self.nome} executou ação: {acao}"

class MonarcaAbsoluto(Personagem):
    """Protagonista - Monarca Caíque (OWNER), com atributos de APOLO."""
    def __init__(self, nome: str, base: 'BaseMilitar'):
        super().__init__(nome, cargo="OWNER", raca="Humano", classe="Comandante", base=base)
        self.volicao = 9999
        self.moral = 100.0
        self.indice_dimensional = 3.0
        self.harem = {"Luna": 100, "Seo-Yeon": 99, "Calia Cardinal": 100, "Maria": 95}
        self.rank = "LEGENDA"
        self.nivel = 999
        self.hp = 9999 # Monarca é quase invencível por natureza

    def ativar_volicao(self):
        """Mecânica Agony Overflow."""
        if self.moral < 20:
            self.indice_dimensional += 0.5
            self.moral = 70
            print(f"\n⚡ AGONY OVERFLOW ATIVADO! A dor me torna mais forte.")
            print(f"   NOVO ÍNDICE DIMENSIONAL: {self.indice_dimensional:.2f}")
            return True
        return False

    def sinergia_harem(self):
        """Restaura a moral com base no número de entidades submissas."""
        bonus = len(self.harem) * 12
        self.moral = min(100, self.moral + bonus)
        # print(f"SINERGIA DE SUBMISSÃO: {len(self.harem)} almas me servem. Moral restaurada +{bonus}")

# ===================== INIMIGO (PODER PSICOLÓGICO) =====================
class Inimigo(Personagem):
    def __init__(self, nome, cargo='Geral Inimigo', raca='Demônio', nivel_ameaca=65, poder_psicologico=True, pos=(0,0)):
        super().__init__(nome, cargo, raca, classe='Mago')
        self.hp = 150
        self.nivel_forca = nivel_ameaca
        self.poder_psicologico = poder_psicologico
        self.dano_base = 35
        self.pos = pos

    def usar_poder(self, alvo: MonarcaAbsoluto):
        """Ataca o alvo com dano psicológico, mitigado pela defesa SSSS da Base."""
        if self.poder_psicologico:
            dano_base = self.nivel_forca * 0.75

            if alvo.cargo == 'OWNER' and alvo.base:
                defesa_pct = alvo.base.defesa_psiquica
                dano_final = dano_base * (1.0 - defesa_pct)

                alvo.moral = max(0, alvo.moral - dano_final)
                alvo.humor = "dominado_psicologicamente"

                print(f"⚠️ [DANO PSICOLÓGICO]: {self.nome} usou Manipulação Mental.")
                print(f"   Mitigação SSSS: {defesa_pct*100:.0f}% aplicada. Dano de Moral Recebido: {dano_final:.1f}")
                return 'PSICOLOGICO', alvo.moral
        return 'IDLE', None

# ===================== BASE MILITAR (HUB & ESTRUTURAS) =====================
class ComponenteBase:
    """Subsistema interno do CORE NEXUS AURORA."""
    def __init__(self, nome: str, tipo: str, consumo_mana: int, producao_recurso: Optional[Dict[str, int]] = None):
        self.nome = nome
        self.tipo = tipo
        self.status = "OPERACIONAL"
        self.consumo_mana = consumo_mana
        self.producao_recurso = producao_recurso if producao_recurso is not None else {}
        self.nivel_integridade = 100

class BaseMilitar:
    def __init__(self, nome, owner, economia, pos):
        self.nome = nome
        self.owner = owner
        self.economia = economia # Referência à economia cósmica
        self.pos = pos
        self.recursos = self.economia.reservas # Linka diretamente à economia global
        self.tecnologia = Tecnologia()
        self.defesa_psiquica = 0.0 # 0.0 a 0.5 (Mitigação SSSS)
        self.componentes: List[ComponenteBase] = []
        self._inicializar_componentes()

    def _inicializar_componentes(self):
        """Define os componentes centrais da base (APOLO Ω)."""
        self.componentes.append(ComponenteBase("Reator de Éter Ω", "Energia", 10, {'eter': 500, 'mana': 150}))
        self.componentes.append(ComponenteBase("Laboratório SSSS", "Pesquisa", 200, {'materia_escura_ssss': 50}))
        self.componentes.append(ComponenteBase("Jardim Dimensional de Calia", "Suporte_Harem", 50, {}))

    def ciclo_base(self):
        """Processa o consumo e a produção de todos os componentes internos da base."""
        consumo_total_mana = 0
        producao_total = {}

        for comp in self.componentes:
            if comp.status == "OPERACIONAL":
                consumo_total_mana += comp.consumo_mana
                for recurso, quantidade in comp.producao_recurso.items():
                    producao_total[recurso] = producao_total.get(recurso, 0) + quantidade

        self.recursos['mana'] -= consumo_total_mana
        for recurso, quantidade in producao_total.items():
            self.recursos[recurso] = self.recursos.get(recurso, 0) + quantidade

        print(f"  Consumo de MANA da Base: -{consumo_total_mana} | Produção de Recursos: {producao_total}")

    def aplicar_upgrade_psiquico(self):
        """Ativa a defesa SSSS após pesquisa."""
        custo_ssss = 30
        if "Campo Psíquico SSSS" in self.tecnologia.arvore and self.recursos.get("materia_escura_ssss", 0) >= custo_ssss:
            self.recursos["materia_escura_ssss"] -= custo_ssss
            self.defesa_psiquica = 0.50 # 50% de mitigação
            print("🛡️ [UPGRADE ATIVO]: Campo de Estabilidade Psíquica SSSS ativado! Redução de dano psicológico em 50%.")
            return True
        else:
             print("❌ Falha ao ativar: Requisitos do Campo Psíquico SSSS não atendidos.")
             return False

# ===================== FRASES DE COMPORTAMENTO (CÓDIGO DE CONFIRMAÇÃO) =====================
def gerar_codigo_confirmacao(acao: str, cargo: str, nivel_tec: int) -> str:
    """Gera um hash de confirmação para comandos críticos."""
    raw = f"{acao}-{cargo}-{nivel_tec}:{datetime.now().microsecond}"
    return hashlib.sha256(raw.encode()).hexdigest()[:8].upper()

# ===================== AI NPC (INTELIGÊNCIA DE SUPORTE AVANÇADA) =====================
class AI_NPC_Suporte(Personagem):
    """Representa um aliado (como Maria ou Luna) com inteligência tática."""
    def __init__(self, nome, classe, base):
        super().__init__(nome, cargo="Aliado", raca="Humano", classe=classe, base=base)

    def tomar_decisao_suporte(self, monarca: MonarcaAbsoluto, inimigo: Inimigo):
        """Delibera ações baseadas no estado do Monarca."""

        # Estratégia 1: Suporte Psicológico (Prioridade Máxima)
        if monarca.humor == "dominado_psicologicamente" or monarca.moral < 40:
            if monarca.base and monarca.base.defesa_psiquica < 0.5:
                 print(f"[{self.nome} - SUPORTE]: Prioridade! Necessário ativar Campo Psíquico SSSS na base.")
                 monarca.base.aplicar_upgrade_psiquico()
                 return 'ATIVAR_DEFESA_PSÍQUICA'

            # Ação de Restauração de Moral (Sinergia de campo)
            if self.classe == 'Clérigo' or self.classe == 'Mago':
                monarca.moral = min(100, monarca.moral + 15)
                print(f"[{self.nome} - SUPORTE]: Usando Sinergia de Vontade. Moral do Monarca restaurada (+15).")
                return 'RESTAURAR_MORAL'

        # Estratégia 2: Combate Tático
        if inimigo and inimigo.hp > 0:
            return self.agir('atacar', inimigo)

        return 'IDLE'

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
        self.dominio = 0.0

    def ciclo(self):
        self.turno += 1
        print(f"\n{'='*110}")
        print(f"                  CICLO {self.turno} — DOMÍNIO ABSOLUTO DO MONARCA CAÍQUE")
        print(f"{'='*110}")

        # 1. Manutenção de Sistemas
        self.economia.ciclo_ganho()
        self.base.ciclo_base()
        self.cardinal.salvar_realidade(self.protagonista, self.economia)

        # 2. Ações do Protagonista
        self.protagonista.ativar_volicao() # Agony Overflow
        if self.turno % 3 == 0:
            self.protagonista.sinergia_harem()

        # 3. Conflito (Combate Psicológico e Suporte)
        if self.inimigos:
            inimigo_atual = self.inimigos[0]

            # A. Ação do Inimigo (Dano Psicológico)
            inimigo_atual.usar_poder(self.protagonista)

            # B. Ação do Aliado (Suporte Inteligente)
            for aliado in self.aliados:
                aliado.tomar_decisao_suporte(self.protagonista, inimigo_atual)

            # C. Resposta do Protagonista (Ataque)
            msg = self.protagonista.agir('atacar', inimigo_atual)
            print(f"  Ação Monarca: {msg}")

            if inimigo_atual.hp <= 0:
                print(f"🎉 Vitória! {inimigo_atual.nome} foi erradicado.")
                self.inimigos.pop(0)

        # 4. Cálculo de Domínio Cósmico
        self.dominio += 77.7 + (self.protagonista.indice_dimensional * 33)

        # 5. Relatório de Status
        print(f"\n--- RELATÓRIO CHAVE (Monarca e Base) ---")
        print(f"  Moral: {self.protagonista.moral:.1f}/100 | Índice Dimensional: {self.protagonista.indice_dimensional:.2f}")
        print(f"  Domínio Cósmico: {self.dominio:.1f}% | Inimigos Restantes: {len(self.inimigos)}")
        print(f"  Defesa Psíquica SSSS: {self.base.defesa_psiquica * 100:.0f}% Ativa")
        print(f"  Recursos (M. Escura/Éter): {self.economia.reservas['materia_escura_ssss']}/{self.economia.reservas['eter']}")

        codigo = gerar_codigo_confirmacao("ASSALTO_FINAL", self.protagonista.cargo, self.base.tecnologia.nivel)
        print(f"  [PROTOCOLO]: Comando ASSALTO_FINAL. Código de Confirmação: {codigo}")

# ============================= EXECUÇÃO FINAL & TESTE =============================
if __name__ == "__main__":
    print("\n" + "="*100)
    print("             BEM-VINDO AO DOMÍNIO TOTAL, MONARCA CAÍQUE (V2.0)")
    print("="*100)
    time.sleep(3)

    jogo = Engine()

    # Preparação: Pesquisa do campo Psíquico SSSS antes do combate
    print("\n🔬 INICIANDO PESQUISA CRÍTICA...")
    custo_pesquisa = {"materia_escura_ssss": 50, "eter": 100}
    jogo.base.tecnologia.pesquisar("Campo Psíquico SSSS", custo_pesquisa, jogo.base)
    time.sleep(1)

    try:
        while jogo.turno < 5 and jogo.inimigos: # Limita a 5 ciclos para o teste
            jogo.ciclo()
            time.sleep(1.8)
    except KeyboardInterrupt:
        pass

    print(f"\n\nDOMÍNIO TOTAL ALCANÇADO APÓS {jogo.turno} CICLOS.")
    print(f"Domínio Final: {jogo.dominio:.1f}%")
    print(f"Realidades salvas pela Cardinal: {jogo.cardinal.correcoes}")
    print(f"Índice Dimensional Final: {jogo.protagonista.indice_dimensional:.2f}")
    print("\nObrigado por tudo, Monarca Caíque. Você venceu.")
