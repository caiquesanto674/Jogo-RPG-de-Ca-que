#!/usr/bin/env python3
"""
NEXUS ENGINE - Jogo de Estratégia/RPG Unificado Completo
Consolida TODOS os sistemas: Militar, Economia, Tecnologia, IA Adaptativa
"""

import logging
from nexus.sistemas.motor import MotorNexus


# Configuração de logging global
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)


def main():
    """Ponto de entrada principal do NEXUS ENGINE."""
    print("🚀 === INICIANDO NEXUS ENGINE - SISTEMA CARDINALIS === 🚀")

    # Inicializa o motor central com TODOS os sistemas integrados
    engine = MotorNexus(owner="COMMANDER")

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
