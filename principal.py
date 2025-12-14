# -*- coding: utf-8 -*-

from apolo_engine.sistemas.motor_decisao import SistemaDecisaoFonte
from apolo_engine.sistemas.ambiente import Mundo, ServicoGPS, ServicoDeTempo
from apolo_engine.entidades.unidades import Personagem, Inimigo
from apolo_engine.entidades.item import Item
from apolo_engine.ia.assistentes import (
    AssistenteSupervisionado,
    AssistenteReforco,
    AssistenteAutoSupervisionado,
)

# ==============================================================================
# FUNÇÃO PRINCIPAL E LOOP DE JOGO
# ==============================================================================

def main():
    """ Ponto de entrada principal do programa. """
    # --- Inicialização ---
    print("--- INICIALIZANDO O SISTEMA DE RPG ---")
    sdf = SistemaDecisaoFonte()
    servico_gps = ServicoGPS()
    servico_tempo = ServicoDeTempo()
    mundo = Mundo(servico_gps=servico_gps, servico_tempo=servico_tempo)

    ia_supervisionada = AssistenteSupervisionado()
    ia_reforco = AssistenteReforco()
    ia_autossupervisionada = AssistenteAutoSupervisionado()

    jogador = Personagem("Herói", 10, 100)
    monstro = Inimigo("Ogro", 5, 80, assistente_ia=ia_reforco)
    mundo.adicionar_entidade(jogador)
    mundo.adicionar_entidade(monstro)

    jogador.inventario.adicionar_item(ia_autossupervisionada.gerar_item_aleatorio())
    monstro.inventario.adicionar_item(Item("Poção de Cura Simples", "pocao"))

    # --- Início do Combate ---
    print("\n--- COMBATE INICIADO ---")
    print(f"{monstro.nome}: '{ia_supervisionada.gerar_dialogo('inicio_combate')}'\n")

    while jogador.vida > 0 and monstro.vida > 0:
        # --- Turno do Jogador ---
        print(f"--- Turno do Jogador (Vida: {jogador.vida}) ---")
        monstro.memoria.limpar_memoria_curto_prazo()
        acao = input("O que você faz? (atacar / usar pocao): ").lower()
        if acao == "atacar":
            jogador.atacar(monstro, sdf)
        elif acao == "usar pocao":
            jogador.usar_pocao(sdf)
        else:
            print("Ação inválida!")
            continue

        if monstro.vida <= 0:
            break

        # --- Turno do Inimigo ---
        print(f"\n--- Turno do Inimigo (Vida: {monstro.vida}) ---")
        acao_ia = monstro.assistente_ia.tomar_decisao_combate(monstro, jogador)
        if acao_ia == "atacar":
            monstro.atacar(jogador, sdf)
        elif acao_ia == "usar pocao":
            monstro.usar_pocao(sdf)

        print("-" * 20)

    # --- Fim do Combate ---
    print("\n--- COMBATE FINALIZADO ---")
    if jogador.vida > 0:
        print(f"O {jogador.nome} foi vitorioso!")
        print(f"{monstro.nome}: '{ia_supervisionada.gerar_dialogo('fim_combate')}'")
    else:
        print(f"O {monstro.nome} foi vitorioso!")

if __name__ == "__main__":
    main()
