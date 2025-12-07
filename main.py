import time
from engine.motor import Engine

# ============================= EXECUÇÃO FINAL & TESTE =============================
if __name__ == "__main__":
    print("\n" + "="*100)
    print("             INICIANDO APOLO MEGA SYSTEM FINAL (V2.0.1)")
    print("="*100)

    jogo = Engine()

    # Preparação: Pesquisa do campo Psíquico SSSS antes do combate
    custo_pesquisa = {"materia_escura_ssss": 50, "eter": 100}
    jogo.base.tecnologia.pesquisar("Campo Psíquico SSSS", custo_pesquisa, jogo.base)

    try:
        while jogo.turno < 4:
            jogo.ciclo()
            time.sleep(1.8)
    except KeyboardInterrupt:
        pass

    print("\n\nSIMULAÇÃO FINALIZADA. Domínio mantido.")
