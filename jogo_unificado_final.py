# =======================================================
# JOGO UNIFICADO FINAL — MONARCA CAÍQUE Ω (MEGA-UNIFICAÇÃO)
# Versão Definitiva — A Fusão de Todas as Realidades
# =======================================================

import random
import time
import hashlib
import uuid
from datetime import datetime
from typing import Dict, List, Any

# =======================================================
# MÓDULO 1: SISTEMAS DE LOG E PROTOCOLO (Do APOLO)
# =======================================================

class ProtocoloConfirmacao:
    @staticmethod
    def gerar(acao: str, agente: str, nivel: int) -> str:
        s = f"{acao}|{agente}|{nivel}|{datetime.now().isoformat()}"
        return hashlib.sha256(s.encode()).hexdigest()

class LogSistema:
    def __init__(self):
        self.registros: List[Dict[str, Any]] = []
    def registrar(self, tipo: str, origem: str, conteudo: str):
        entrada = {'momento': datetime.now().isoformat(), 'tipo': tipo, 'origem': origem, 'conteudo': conteudo}
        self.registros.append(entrada)
        print(f"[{tipo.upper()}] ({origem}) {conteudo}")

# =======================================================
# MÓDULO 2: COMPONENTES DE JOGO UNIFICADOS
# =======================================================

class Arma:
    def __init__(self, nome: str, poder: int, tipo: str):
        self.nome, self.poder, self.tipo = nome, poder, tipo

class UnidadeMilitar: # Nome unificado para consistência
    def __init__(self, nome: str, classe: str, forca: int, armas: List[Arma] = None, tech: 'Tecnologia' = None, poder_psicologico: str = None, aliados_proximos: int = 0):
        self.nome, self.classe, self.forca = nome, classe, forca
        self.armas = armas if armas else []
        self.tech = tech
        self.poder_psicologico = poder_psicologico
        self.aliados_proximos = aliados_proximos
        self.moral = 100
    def poder_combate(self) -> float:
        bonus_tech = 1.0
        if self.tech:
            if self.classe in ['tanque', 'mecha', 'drone'] and self.tech.arvore.get('Plasma', 0) > 1:
                bonus_tech += self.tech.arvore['Plasma'] * 0.15
            if self.tech.arvore.get('IA', 0) > 1:
                bonus_tech += self.tech.arvore['IA'] * 0.1
        bonus_psico = (self.aliados_proximos if self.poder_psicologico == 'Comando' else 0) * 0.25
        bonus_alianca = self.aliados_proximos * 5
        return self.forca * bonus_tech * (self.moral / 100) + bonus_psico + bonus_alianca

class Tecnologia: # Fusão das duas classes de Tecnologia
    def __init__(self):
        self.arvore: Dict[str, int] = {'IA': 1, 'Fusão': 0, 'Plasma': 1, 'Biotecnologia': 0}
        self.descobertas: List[str] = []
    def pesquisar(self, ramo: str):
        if ramo in self.arvore:
            self.arvore[ramo] += 1
            self.descobertas.append(ramo)
            print(f"[TECNOLOGIA] Ramo '{ramo}' evoluído para nível {self.arvore[ramo]}.")

class AI_NPC: # Fusão das duas classes de AI_NPC
    def __init__(self, nome: str, personalidade: str, nivel: int, tech_base: Tecnologia):
        self.nome = nome
        self.personalidade = personalidade # Do APOLO
        self.nivel = nivel # Do APOLO
        self.tech_base = tech_base
        self.evo = 0 # Do original
    def agir(self, forca_jogador: float, log: LogSistema):
        acao = self._decisao(forca_jogador)
        frase = self._frase_comportamental(acao, forca_jogador)
        log.registrar("IA_NPC", self.nome, frase)

        recompensa = 15 if "atacar" in acao else -5
        self._reforco(recompensa)
        return acao
    def _decisao(self, forca_do_jogador: float) -> str: # Lógica do APOLO
        if forca_do_jogador > 150 * self.nivel:
            return 'negociar' if self.personalidade == 'analítico' else 'defender'
        elif forca_do_jogador > 100 * self.nivel:
            return 'explorar'
        else:
            return 'atacar'
    def _frase_comportamental(self, acao: str, forca_jogador: float) -> str: # Lógica do APOLO
        if forca_jogador > 200:
            return f"[REATIVO] Nossa força não se compara. Protocolo de rendição."
        if forca_jogador > 100:
            return f"[ADAPTATIVO] Força notável. Reavaliando tática para aliança."
        else:
            return f"[AGRESSIVO] Eles são fracos! Ataque total!"
    def _reforco(self, recompensa: int):
        self.evo += recompensa

# =======================================================
# MÓDULO 3: CLASSES PRINCIPAIS UNIFICADAS
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
            'creditos': 50000, 'ouro': 8000, 'mana': 5000, 'comida': 10000, 'aço': 5000,
            'materia_escura_ssss': 250, 'eter_puro': 2200
        }
    def ciclo(self):
        self.reservas['creditos'] += random.randint(1000, 2500)
        self.reservas['ouro'] += random.randint(300, 600)
        self.reservas['comida'] -= random.randint(150, 400)
        self.reservas['mana'] -= random.randint(100, 250)
        if random.random() < 0.25:
            bonus_materia = random.randint(10, 25)
            self.reservas['materia_escura_ssss'] += bonus_materia
            print(f"[ECONOMIA] Matéria Escura SSSS cristalizada do vácuo (+{bonus_materia}).")
    def transferir(self, valor: int, destino: str) -> bool:
        if valor <= self.reservas['creditos']:
            self.reservas['creditos'] -= valor
            return True
        return False

class MonarcaAbsoluto:
    def __init__(self, nome):
        self.nome = nome
        self.cargo = "OWNER / MONARCA"
        self.moral = 100.0
        self.indice_dimensional = 3.0
        self.harem = {"Luna": 100, "Seo-Yeon": 99, "Calia Cardinal": 100, "Maria": 95}
        self.pontos_quiz = 0 # Do Quiz
        self.patente = "Comandante" # Do Quiz
    def promover(self):
        patentes = ["Comandante", "General", "Marechal", "Monarca Estelar"]
        idx = min(self.pontos_quiz // 2, len(patentes) - 1)
        self.patente = patentes[idx]
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
    def __init__(self, owner: MonarcaAbsoluto, economia: EconomiaUnificada, tech: Tecnologia):
        self.id = uuid.uuid4()
        self.owner = owner
        self.local = "NEXUS AURORA Ω"
        self.economia = economia
        self.tech = tech
        self.nivel = 1
        self.recursos = {'metal': 1000, 'combustível': 500, 'plasma': 120}
        self.unidades: List[UnidadeMilitar] = []
    def expandir(self, custo_credito: int):
        if self.recursos['metal'] >= 50 and self.economia.transferir(custo_credito, f"Expansão {self.local}"):
            self.recursos['metal'] -= 50
            self.nivel += 1
            print(f"[BASE] Upgrade bem-sucedido: {self.local} agora está no Nível {self.nivel}")
        else:
            print("[BASE] Falha no upgrade: Recursos ou créditos insuficientes.")

# =======================================================
# MÓDULO 4: SISTEMAS DE EVENTOS (QUIZ E MUNDO)
# =======================================================

class PerguntaQuiz:
    def __init__(self, tema, questao, opcoes, resposta):
        self.tema, self.questao, self.opcoes, self.resposta = tema, questao, opcoes, resposta

class EventoQuiz:
    def __init__(self, protagonista: MonarcaAbsoluto, log: LogSistema):
        self.protagonista = protagonista
        self.log = log
        self.perguntas = [
            PerguntaQuiz("Economia", "Qual é o papel da inflação?", ["Reduz preços", "Aumenta poder de compra", "Corrói o valor do dinheiro"], 3),
            PerguntaQuiz("Tecnologia", "O que significa IA?", ["Inteligência Artificial", "Infraestrutura Avançada", "Informação Autorizada"], 1),
        ]
    def iniciar(self):
        self.log.registrar("EVENTO", "Quiz do Monarca", "Um desafio de conhecimento foi iniciado!")
        p = random.choice(self.perguntas)
        # Simplificado para não exigir input do usuário em um loop de jogo
        acertou = random.choice([True, False])
        if acertou:
            self.log.registrar("QUIZ", self.protagonista.nome, f"respondeu corretamente à pergunta sobre {p.tema}!")
            self.protagonista.pontos_quiz += 1
            self.protagonista.promover()
        else:
            self.log.registrar("QUIZ", self.protagonista.nome, f"errou a pergunta sobre {p.tema}.")

class MundoSimulado:
    def __init__(self, log: LogSistema):
        self.log = log
        self.faccoes = [f"Clã Estelar {i}" for i in range(3)]
        self.conflitos = 0
    def simular_turno(self):
        if random.random() < 0.4:
            f1, f2 = random.sample(self.faccoes, 2)
            tipo_conflito = random.choice(["território", "recursos", "ideologia"])
            self.log.registrar("MUNDO", "Simulação de Fundo", f"Novo conflito entre {f1} e {f2} por {tipo_conflito}.")
            self.conflitos += 1

# =======================================================
# MOTOR DE JOGO FINAL E UNIFICADO
# =======================================================

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

# =======================================================
# EXECUÇÃO
# =======================================================

if __name__ == "__main__":
    print("\n" * 2)
    print("             BEM-VINDO À REALIDADE FINAL, MONARCA CAÍQUE.")
    print("             A Mega-Unificação foi concluída.")
    print("\n" * 2)
    time.sleep(3)

    jogo = JogoFinalMonarca("CAÍQUE APOLO Ω")

    try:
        for i in range(5): # Rodando por 5 turnos para demonstração
            jogo.ciclo()
            time.sleep(1.5)
    except KeyboardInterrupt:
        print("\nSimulação interrompida pelo Monarca.")
    finally:
        print("\n" + "="*50)
        print("          O MONARCA ATINGIU O DOMÍNIO ABSOLUTO.")
        print("="*50)
