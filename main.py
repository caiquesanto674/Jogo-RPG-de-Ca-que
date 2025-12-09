# main.py
# Ponto de Entrada para o Monarca Omega Engine

import time
from src.engine import JogoFinalMonarca

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
