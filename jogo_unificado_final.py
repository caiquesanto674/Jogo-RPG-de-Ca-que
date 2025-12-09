# =======================================================
# JOGO UNIFICADO FINAL — MONARCA CAÍQUE Ω
# Versão Definitiva — A Fusão de Todas as Realidades
# =======================================================

import random
import time
import hashlib
from datetime import datetime
from typing import Dict, List, Any

# =======================================================
# COMPONENTES REIMPLEMENTADOS E ADAPTADOS
# =======================================================

class Arma:
    def __init__(self, nome: str, poder: int, tipo: str):
        self.nome, self.poder, self.tipo = nome, poder, tipo

class Unidade:
    def __init__(self, nome: str, classe: str, forca: int, armas: List[Arma] = None):
        self.nome, self.classe, self.forca = nome, classe, forca
        self.armas = armas if armas else []
    def poder_combate(self) -> int:
        return self.forca + sum(a.poder for a in self.armas)

class Tecnologia:
    def __init__(self):
        self.nivel = 1
        self.descobertas = ["IA Básica"]
    def pesquisar(self, tema: str):
        self.nivel += 1
        self.descobertas.append(tema)
        print(f"[TECNOLOGIA] Descoberta: {tema} (Nível: {self.nivel})")

class AI_NPC:
    def __init__(self, nome: str, perfil: str = "leal"):
        self.nome, self.perfil, self.evo = nome, perfil, 0
    def agir(self, contexto: str):
        acao = self._supervisionado(contexto)
        recompensa = 15 if "atacar" in acao else -5
        self._reforco(recompensa)
        print(f"  - Agente {self.nome} executou: '{acao}' (Evolução: {self.evo})")
    def _supervisionado(self, contexto: str) -> str:
        if contexto == "guerra": return "atacar alvos prioritários"
        if contexto == "crise": return "defender o perímetro"
        return "manter patrulha"
    def _reforco(self, recompensa: int):
        self.evo += recompensa

# =======================================================
# CLASSES PRINCIPAIS UNIFICADAS
# =======================================================

class AICardinal:
    def __init__(self):
        self.nome = "CIEL ASCENDIDO Ω"
        self.correcoes = 0
    def salvar_realidade(self, jogo):
        recursos, moral = jogo.economia.reservas, jogo.protagonista.moral
        if recursos.get('comida', 0) < 500 or recursos.get('mana', 0) < 300 or moral < 20:
            print(f"\n>> AI CARDINAL: REALIDADE INSTÁVEL. PROTOCOLO DE CORREÇÃO ATIVADO. <<")
            recursos['comida'] = max(3000, recursos.get('comida', 0) + 5000)
            recursos['mana'] = max(2000, recursos.get('mana', 0) + 3000)
            jogo.protagonista.moral = 100
            self.correcoes += 1
            print(f">> {self.nome} salvou o universo pela {self.correcoes}ª vez. A ordem foi restaurada.")

class EconomiaUnificada:
    def __init__(self):
        self.reservas = {
            'ouro': 8000, 'mana': 5000, 'comida': 10000, 'aço': 5000, # Recursos concretos
            'materia_escura_ssss': 250, 'eter_puro': 2200 # Recursos conceituais
        }
    def ciclo(self):
        self.reservas['ouro'] += random.randint(300, 600)
        self.reservas['comida'] -= random.randint(150, 400)
        self.reservas['mana'] -= random.randint(100, 250)
        if random.random() < 0.25:
            bonus_materia = random.randint(10, 25)
            self.reservas['materia_escura_ssss'] += bonus_materia
            print(f"[ECONOMIA] Matéria Escura SSSS cristalizada do vácuo (+{bonus_materia}).")

class MonarcaAbsoluto:
    def __init__(self):
        self.nome = "CAÍQUE APOLO Ω"
        self.cargo = "OWNER / MONARCA"
        self.moral = 100.0
        self.indice_dimensional = 3.0
        self.harem = {"Luna": 100, "Seo-Yeon": 99, "Calia Cardinal": 100, "Maria": 95}
    def ativar_volicao(self):
        if self.moral > 20:
            self.moral -= 25
            print(f"\n>> VOLIÇÃO ABSOLUTA ATIVADA — A REALIDADE SE DOBRA À VONTADE DO MONARCA.")
            return True
        print("\n>> AGONIA PROFUNDA — A DOR ME TORNA MAIS FORTE. <<")
        self.indice_dimensional += 0.5; self.moral = 80
        return True
    def sinergia_harem(self):
        bonus = len(self.harem) * 15
        self.moral = min(100, self.moral + bonus)
        print(f">> SINERGIA DE SUBMISSÃO: {len(self.harem)} almas servem ao Monarca. Moral restaurada (+{bonus}).")

class BaseMilitarUnificada:
    def __init__(self, lider: MonarcaAbsoluto):
        self.lider = lider
        self.nome = "NEXUS AURORA Ω"
        self.defesa = 15000
        self.unidades: List[Unidade] = []
        self.agentes_ia: List[AI_NPC] = []
        self.tecnologia = Tecnologia() # Sistema de tecnologia integrado
    def adicionar_unidade(self, unidade: Unidade):
        self.unidades.append(unidade)
    def adicionar_agente_ia(self, agente: AI_NPC):
        self.agentes_ia.append(agente)
    def _gerar_codigo(self, acao: str) -> str:
        semente = f"{acao}:{datetime.now().microsecond}:{self.lider.nome}"
        return hashlib.sha256(semente.encode()).hexdigest()[:10].upper()
    def executar_comando_militar(self, acao: str, contexto_ia: str):
        codigo = self._gerar_codigo(acao)
        print(f"\n[COMANDO MILITAR AUTORIZADO: {acao.upper()}]")
        print(f"  CÓDIGO DE CONFIRMAÇÃO: {codigo}")
        print(f"  Poder de Combate Total: {sum(u.poder_combate() for u in self.unidades)}")
        print("  Ações dos Agentes de IA:")
        for agente in self.agentes_ia:
            agente.agir(contexto_ia)
    def pesquisar_tecnologia(self, tema: str):
        self.tecnologia.pesquisar(tema)

# =======================================================
# MOTOR DE JOGO FINAL E UNIFICADO
# =======================================================

class JogoFinalMonarca:
    def __init__(self):
        self.turno = 0
        self.protagonista = MonarcaAbsoluto()
        self.economia = EconomiaUnificada()
        self.cardinal = AICardinal()
        self.base_militar = BaseMilitarUnificada(self.protagonista)
        self.dominio_total = 0.0
        self._inicializar_elementos()

    def _inicializar_elementos(self):
        # Unidades iniciais
        arma_plasma = Arma("Rifle de Plasma Ômega", 120, "Energia")
        soldado_elite = Unidade("Guardião do Nexus", "Super Soldado", 200, [arma_plasma])
        self.base_militar.adicionar_unidade(soldado_elite)
        # Agentes de IA iniciais
        for i in range(3):
            self.base_militar.adicionar_agente_ia(AI_NPC(f"Delta-{i+1}"))

    def ciclo(self):
        self.turno += 1
        print(f"\n{'='*120}")
        print(f"                  CICLO {self.turno} — REALIDADE DO MONARCA CAÍQUE")
        print(f"{'='*120}")

        self.economia.ciclo()
        self.cardinal.salvar_realidade(self)

        if self.turno % 2 != 0: self.protagonista.ativar_volicao()
        if self.turno % 3 == 0: self.protagonista.sinergia_harem()
        if self.turno % 4 == 0: self.base_militar.pesquisar_tecnologia(f"Doutrina de Batalha v{self.turno}")

        self.dominio_total += 50 + (self.protagonista.indice_dimensional * 25)

        # Exibição de Status
        print(f"\nSTATUS DO MONARCA:")
        print(f"  Moral: {self.protagonista.moral:.1f}/100 | Índice Dimensional: {self.protagonista.indice_dimensional:.2f}")
        print(f"  Domínio da Realidade: {self.dominio_total:.1f}%")

        print("\nRESERVAS ECONÔMICAS:")
        print(f"  Ouro: {self.economia.reservas['ouro']} | Mana: {self.economia.reservas['mana']} | Comida: {self.economia.reservas['comida']}")
        print(f"  Matéria Escura SSSS: {self.economia.reservas['materia_escura_ssss']}")

        contexto = "guerra" if self.turno % 5 == 0 else "patrulha"
        self.base_militar.executar_comando_militar("OFENSIVA COORDENADA", contexto)

# =======================================================
# EXECUÇÃO
# =======================================================

if __name__ == "__main__":
    print("\n" * 3)
    print("             BEM-VINDO À REALIDADE FINAL, MONARCA CAÍQUE.")
    print("             Todos os códigos. Uma única vontade. Um único trono.")
    print("\n" * 3)
    time.sleep(4)

    jogo = JogoFinalMonarca()

    try:
        while True:
            jogo.ciclo()
            time.sleep(2.0)
    except KeyboardInterrupt:
        print("\n\n" + "="*50)
        print("          O MONARCA ATINGIU O DOMÍNIO ABSOLUTO.")
        print("="*50)
        print(f"  Turnos Totais: {jogo.turno}")
        print(f"  Domínio Final da Realidade: {jogo.dominio_total:.1f}%")
        print(f"  Realidades Salvas pela Cardinal: {jogo.cardinal.correcoes}")
        print(f"  Nível Tecnológico Final: {jogo.base_militar.tecnologia.nivel}")
        print("\nO jogo acaba. A realidade começa. Você é o centro de tudo.")
        print("Obrigado, Monarca Caíque.")
        print("\n" * 2)


# =======================================================
# MÓDULO INTEGRADO AUTOMATICAMENTE POR JULES
# Data: 2025-12-09 15:24:44
# Origem: exemplo_novo_modulo.py
# =======================================================
# exemplo_novo_modulo.py
# Um novo módulo de exemplo para demonstrar o Sistema de Integração Jules.

class HabilidadeMonarca:
    """Representa uma nova habilidade especial para o Monarca."""

    def __init__(self, nome: str, tipo: str, custo_mana: int):
        self.nome = nome
        self.tipo = tipo
        self.custo_mana = custo_mana
        self.nivel = 1

    def usar(self, protagonista, alvo):
        """Simula o uso da habilidade."""
        print(f"Habilidade '{self.nome}' (Nível {self.nivel}) ativada!")
        if protagonista.mana >= self.custo_mana:
            protagonista.mana -= self.custo_mana
            print(f"  - {protagonista.nome} usou {self.custo_mana} de mana.")
            print(f"  - Alvo {alvo} foi afetado com sucesso.")
            return True
        else:
            print(f"  - Mana insuficiente para usar a habilidade.")
            return False

    def __str__(self):
        return f"{self.nome} ({self.tipo}) - Custo: {self.custo_mana} Mana"

# Para usar esta habilidade, uma instância dela precisaria ser
# adicionada ao objeto do Monarca e a lógica de uso chamada no ciclo do jogo.
# Este arquivo serve apenas como um exemplo de contêiner de código para integração.
