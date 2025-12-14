#!/usr/bin/env python3
"""
APOLO ENGINE - Jogo de Estratégia/RPG Unificado Completo
Consolida TODOS os sistemas: Militar, Economia, Tecnologia, IA Adaptativa
"""

import logging
from apolo_engine.systems.motor import Engine_APOLO
# AGENT-DEFINED: Import BaseMilitar to add more bases to the simulation
from apolo_engine.entities.base import BaseMilitar


# Configuração de logging global
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)


def main():
    """Ponto de entrada principal do APOLO ENGINE."""
    print("🚀 === INICIANDO APOLO ENGINE - SISTEMA CARDINALIS === 🚀")

    # Inicializa o motor central com TODOS os sistemas integrados
    engine = Engine_APOLO(owner="COMMANDER")

    # AGENT-DEFINED: Add more bases to the simulation to showcase the new features
    engine.bases.append(BaseMilitar(engine.owner, "Beta Centauri", engine.economia, engine.tech, nivel=2))
    engine.bases.append(BaseMilitar(engine.owner, "Gamma Orionis", engine.economia, engine.tech, nivel=3))

    # AGENT-DEFINED: Set different initial resources for the new bases
    engine.bases[1].recursos = {"metal": 500, "combustível": 200, "plasma": 50}
    engine.bases[2].recursos = {"metal": 2000, "combustível": 1500, "plasma": 300}

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
