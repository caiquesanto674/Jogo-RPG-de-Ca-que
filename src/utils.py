# Versão Final Unificada: Jogo Híbrido (RPG/Tycoon) + Sistemas de Suporte Ω
# Data: 07 Dezembro 2025

import hashlib
from datetime import datetime
from typing import Any, Dict, List

# ===================== CONFIGURAÇÃO GLOBAL E UTILITÁRIOS =====================
MAPA_TAMANHO = (30, 30)


def gerar_codigo_confirmacao(acao: str, cargo: str, nivel_tec: int) -> str:
    """Frases de Comportamento: Gera um hash de confirmação para comandos críticos."""
    raw = f"{acao}-{cargo}-{nivel_tec}:{datetime.now().microsecond}"
    return hashlib.sha256(raw.encode()).hexdigest()[:8].upper()


# ===================== MÓDULO DE SERVIÇOS (DIAGNÓSTICO/CORREÇÃO) =====================


class Diagnostico:
    """Diagnóstico Proativo: Verifica e corrige inconsistências menores antes da falha total."""

    def __init__(self, engine):
        self.engine = engine

    def check_integridade(self):
        """Monitora moral e recursos críticos, acionando alertas proativos."""
        monarca = self.engine.protagonista
        base = self.engine.base

        if monarca.moral < 45 and not monarca.ativacao_overflow:
            print("❗ DIAGNÓSTICO PROATIVO: Moral em nível de risco. Preparar Agony Overflow.")

        if base.recursos.get("Munição", 0) < 5 and base.veiculos:
            print("🛠️ DIAGNÓSTICO: Estoque de Munição CRÍTICO. Iniciando produção emergencial.")
            base.recursos["Munição"] += 5


class CorrecaoLog:
    """Contabiliza e registra as ações do sistema de autocorreção."""

    def __init__(self):
        self.total_conflitos_detectados = 0
        self.total_correcoes_aplicadas = 0
        self.log_registros: List[Dict[str, Any]] = []

    def registrar_conflito(self, arquivo: str):
        self.total_conflitos_detectados += 1
        print(f"🚨 CONFLITO DETECTADO em {arquivo}.")

    def registrar_correcao(self, arquivo: str, decisao: str):
        self.total_correcoes_aplicadas += 1
        print(f"✅ [CORREÇÃO SUCESSO]: {arquivo} resolvido. Decisão: {decisao}")


def auto_correction(engine):
    """Rotina Reativa de Correção de Regras de Jogo."""
    monarca = engine.protagonista
    # Exemplo de Correção de Inconsistência de Hierarquia:
    if monarca.cargo == "OWNER" and monarca.hp < 9999:
        monarca.hp = 9999
        print("🛠️ AUTO-CORREÇÃO: HP do Monarca Absoluto restaurado para o máximo (9999).")
