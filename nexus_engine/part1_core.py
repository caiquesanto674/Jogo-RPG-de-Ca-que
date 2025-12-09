# ============================================================
#  NEXUS ENGINE 7K — MÓDULO CENTRAL
#  Projeto Caíque Multiverso RPG — Versão 1.0
#  Núcleo Universal, Eventos, Causalidade e Fluxo de Tempo
# ============================================================

import uuid
import random
import math
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional


# ============================================================
#  LOG UNIVERSAL — Monitoramento de eventos críticos
# ============================================================

class UniversalLog:
    def __init__(self):
        self.eventos: List[Dict[str, Any]] = []
        self._max_log = 5000

    def registrar(self, origem: str, tipo: str, dados: Dict[str, Any]):
        evento = {
            "id": str(uuid.uuid4()),
            "origem": origem,
            "tipo": tipo,
            "dados": dados,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.eventos.append(evento)

        # Limita tamanho
        if len(self.eventos) > self._max_log:
            self.eventos = self.eventos[-self._max_log:]

    def consultar(self, tipo: Optional[str] = None):
        if tipo is None:
            return self.eventos
        return [e for e in self.eventos if e["tipo"] == tipo]


LOG = UniversalLog()


# ============================================================
#  SISTEMA DE EVENTOS — Base do fluxo do jogo
# ============================================================

class Evento:
    def __init__(self, nome: str, origem: str, gravidade: int = 1, dados: Optional[Dict[str, Any]] = None):
        self.id = str(uuid.uuid4())
        self.nome = nome
        self.origem = origem
        self.gravidade = gravidade
        self.dados = dados or {}
        self.tempo = datetime.utcnow()

    def __repr__(self):
        return f"<Evento {self.nome} ({self.gravidade})>"


class GerenciadorEventos:
    def __init__(self):
        self.fila: List[Evento] = []

    def disparar(self, evento: Evento):
        self.fila.append(evento)
        LOG.registrar(
            origem=evento.origem,
            tipo="evento",
            dados={
                "evento": evento.nome,
                "gravidade": evento.gravidade,
                "dados": evento.dados
            }
        )

    def processar(self):
        eventos_processados = []
        while self.fila:
            evento = self.fila.pop(0)
            eventos_processados.append(evento)

        return eventos_processados


EVENTOS = GerenciadorEventos()


# ============================================================
#  SISTEMA DE TEMPO, CICLOS E FLUXOS CAUSAIS
# ============================================================

class NexusTime:
    """
    Sistema de tempo dinâmico, com múltiplas velocidades,
    ciclos, pausas e manipulação narrativa.
    """

    def __init__(self):
        self.velocidade = 1.0  # 1.0 = tempo normal
        self.tempo_jogo = datetime(3000, 1, 1, 0, 0, 0)
        self.ultimo_tick = datetime.utcnow()

    def tick(self):
        agora = datetime.utcnow()
        delta_real = (agora - self.ultimo_tick).total_seconds()
        self.ultimo_tick = agora

        # avança o tempo interno do jogo
        avancar = delta_real * self.velocidade
        self.tempo_jogo += timedelta(seconds=avancar)

        return self.tempo_jogo

    def definir_velocidade(self, v: float):
        self.velocidade = max(0.01, min(50.0, v))

    def agora(self):
        return self.tempo_jogo


TEMPO = NexusTime()


# ============================================================
#  ENERGIA UNIVERSAL — Base para todas as mecânicas avançadas
# ============================================================

class EnergiaUniversal:
    """
    Energia básica do multiverso, usada em:
    - habilidades
    - IA
    - portais
    - fusão
    - upgrades militares
    """

    def __init__(self, maxima: float = 1000.0, regeneracao: float = 5.0):
        self.maxima = maxima
        self.atual = maxima
        self.regeneracao = regeneracao

    def consumir(self, valor: float) -> bool:
        if valor <= self.atual:
            self.atual -= valor
            return True
        return False

    def regenerar(self):
        self.atual = min(self.maxima, self.atual + self.regeneracao)

    def alterar_maximo(self, novo_max: float):
        self.maxima = max(10.0, novo_max)
        self.atual = min(self.atual, self.maxima)


# ============================================================
#  BASE DE ENTIDADES — Jogadores, NPCs, Unidades, Criaturas
# ============================================================

class Entidade:
    def __init__(self, nome: str, nivel: int = 1):
        self.id = str(uuid.uuid4())
        self.nome = nome
        self.nivel = nivel
        self.hp = 100 + nivel * 10
        self.energia = EnergiaUniversal(500 + nivel * 25)
        self.inventario: List[str] = []
        self.afeto = 0.0
        self.volicao = 1.0

    def receber_dano(self, valor: float):
        self.hp = max(0, self.hp - valor)
        LOG.registrar(
            origem=self.nome,
            tipo="dano",
            dados={"dano": valor, "hp_restante": self.hp}
        )

    def curar(self, valor: float):
        self.hp = min(100 + self.nivel * 10, self.hp + valor)

    def alterar_afeto(self, delta: float):
        self.afeto = max(-100.0, min(100.0, self.afeto + delta))

    def alterar_volicao(self, delta: float):
        self.volicao = max(0.1, min(10.0, self.volicao + delta))

    def __repr__(self):
        return f"<Entidade {self.nome} Nv {self.nivel} HP {self.hp}>"


# ============================================================
#  MOTOR PRINCIPAL DO JOGO (NEXUS ENGINE)
# ============================================================

class NexusEngine:
    """
    Gerencia:
    - tempo
    - eventos
    - entidades
    - IA
    - economia
    - universos
    - sistemas militares
    """

    def __init__(self):
        self.entidades: Dict[str, Entidade] = {}
        self.universos: Dict[str, Any] = {}
        self.iniciado = False

    def iniciar(self):
        if self.iniciado:
            return

        self.iniciado = True
        LOG.registrar("Sistema", "inicio", {"mensagem": "Nexus Engine iniciado."})

    def registrar_entidade(self, entidade: Entidade):
        self.entidades[entidade.id] = entidade
        LOG.registrar(
            origem="Engine",
            tipo="entidade_registrada",
            dados={"id": entidade.id, "nome": entidade.nome}
        )

    def tick(self):
        tempo_atual = TEMPO.tick()
        EVENTOS.processar()
        for e in self.entidades.values():
            e.energia.regenerar()

        return tempo_atual


ENGINE = NexusEngine()
