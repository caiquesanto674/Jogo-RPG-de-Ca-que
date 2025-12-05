import random
import logging
from src.motor_jogo import MotorJogo

def run_game():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
    engine = MotorJogo()
    for i in range(3):
        engine.ciclo_turno(random.choice(["combate","exploracao","crise"]))

    print("-- Últimos logs --")
    for l in engine.log.registros[-5:]:
        print(l)

if __name__ == "__main__":
    run_game()
