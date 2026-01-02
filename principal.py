#!/usr/bin/env python3
"""
APOLO ENGINE - Jogo de Estratégia/RPG Unificado Completo
Consolida TODOS os sistemas: Militar, Economia, Tecnologia, IA Adaptativa
"""

import logging
from apolo_engine.systems.motor import Engine_APOLO


# Configuração de logging global
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)


def main():
    """Ponto de entrada principal do APOLO ENGINE."""
    try:
        print("🚀 === INICIANDO APOLO ENGINE - SISTEMA CARDINALIS === 🚀")

        # Inicializa o motor central com TODOS os sistemas integrados
        engine = Engine_APOLO(owner="COMMANDER")

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
    except Exception:
        # 🛡️ SENTINEL: Captura de exceção global para "Fail Securely"
        # Impede o vazamento de stack traces para o usuário final em caso de falha.
        # Loga a exceção completa para análise de debug.
        logging.error("Ocorreu uma falha crítica e inesperada no motor.", exc_info=True)
        print("\n❌ Ocorreu um erro crítico. A simulação será encerrada.")
        print("Consulte os logs do sistema para mais detalhes.")


if __name__ == "__main__":
    main()
