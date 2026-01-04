#!/usr/bin/env python3
"""
APOLO ENGINE - Jogo de Estratégia/RPG Unificado Completo
Consolida TODOS os sistemas: Militar, Economia, Tecnologia, IA Adaptativa
"""

import logging
import os
from apolo_engine.systems.motor import Engine_APOLO
from apolo_engine.systems.log import LogLevel


# Configuração de logging global
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)


def main():
    """Ponto de entrada principal do APOLO ENGINE."""
    print("🚀 === INICIANDO APOLO ENGINE - SISTEMA CARDINALIS === 🚀")

    # Define o nível de log. Altere para LogLevel.DEBUG para diagnósticos.
    log_level = LogLevel.DEBUG if os.getenv("DEBUG") else LogLevel.INFO

    # Inicializa o motor central com TODOS os sistemas integrados
    engine = Engine_APOLO(owner="COMMANDER", log_level=log_level)

    # Preparação inicial: Evolução tecnológica base
    engine.tech.pesquisar("Plasma")
    engine.tech.pesquisar("IA")

    # Simulação de 5 turnos completos
    for turno in range(1, 6):
        print(f"\n{'='*50}")
        print(f"🎮 TURNO {turno} - ESTADO DO IMPÉRIO")
        print(f"{'='*50}")
        engine.turno_completo()

    # Diagnóstico final completo
    engine.diagnostico_completo()
    print("\n✅ === FIM DA SIMULAÇÃO - MISSÃO CUMPRIDA === ✅")


if __name__ == "__main__":
    main()
