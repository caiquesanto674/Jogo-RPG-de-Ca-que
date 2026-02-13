#!/usr/bin/env python3
"""
APOLO ENGINE - Jogo de Estratégia/RPG Unificado
Ponto de entrada principal que utiliza a arquitetura modular do Apolo Engine.
"""

import logging
from apolo_engine.systems.motor import Engine_APOLO

# Configuração de logging global
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)

def main():
    """Ponto de entrada principal do APOLO ENGINE."""
    print("🚀 === INICIANDO APOLO ENGINE - ARQUITETURA MODULAR === 🚀")

    # Inicializa o motor central com TODOS os sistemas integrados
    engine = Engine_APOLO(owner="COMMANDER")

    # A simulação agora é controlada pelo motor, que já tem um loop definido.
    # O loop em `principal.py` era apenas para demonstração.
    # A lógica de simulação principal pode ser expandida aqui, se necessário.

    # Simulação de 5 turnos completos para demonstração
    for turno in range(1, 6):
        print(f"\n{'='*50}")
        print(f"🎮 TURNO {turno} - ESTADO DO IMPÉRIO")
        print(f"{'='*50}")
        engine.turno_completo()

    # Diagnóstico final completo
    engine.diagnostico_completo()
    print("\n✅ === FIM DA SIMULAÇÃO - ARQUITETURA ESTÁVEL === ✅")

if __name__ == "__main__":
    main()
