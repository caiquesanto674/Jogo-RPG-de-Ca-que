# main.py
import logging
import random

# Importando o motor do jogo e a regra base da nova estrutura
from nexus.sistemas.motor import MotorJogo
from nexus.utils.helpers import regra_base_global

# =========================== CONFIGURAÇÃO E LOG ============================
LOG_JOGO_FILE = "log_nexus_unificado.log"

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler(LOG_JOGO_FILE)],
)


def game_loop_principal():
    """Função principal de execução do jogo."""
    logging.info(f"Iniciando Loop: {regra_base_global()}")
    motor = MotorJogo()

    # Simula 5 turnos com contextos variados
    contextos = ["combate", "crise", "exploracao", "diplomacia", "manutencao"]
    for i in range(1, 6):
        logging.info(f"\n====================== TURNO {i} ======================")
        motor.ciclo_turno(contexto=random.choice(contextos))

    logging.info("\n================== FIM DA SIMULAÇÃO ===================")
    logging.info("Log de Eventos Chave:")
    for data, evento, args in motor.log.registros:
        logging.info(f"[{data.strftime('%H:%M:%S')}] {evento}: {args}")


if __name__ == "__main__":
    game_loop_principal()
