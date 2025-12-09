import time

from src.nexus_core import NexusCore

# ============================= EXECUÇÃO FINAL & TESTE =============================
if __name__ == "__main__":
    print("\n" + "=" * 100)
    print("             INICIANDO APOLO MEGA SYSTEM FINAL (TESTE)")
    print("=" * 100)

    jogo = NexusCore()

    # Preparação: Pesquisa do campo Psíquico SSSS antes do combate
    custo_pesquisa = {"materia_escura_ssss": 50, "eter": 100}
    jogo.base.tecnologia.pesquisar("Campo Psíquico SSSS", custo_pesquisa, jogo.base)

    try:
        for _ in range(3):
            jogo.ciclo()
            time.sleep(1.8)
    except KeyboardInterrupt:
        pass

    print("\n\nSIMULAÇÃO FINALIZADA. Domínio mantido pelo Monarca Caíque.")
