# -*- coding: utf-8 -*-

# ==============================================================================
# 1. IMPORTAÇÕES DOS MÓDULOS DO MOTOR
# ==============================================================================
from motor_apolo.sistemas.motor import (
    SistemaDecisaoFonte, Mundo, ServicoGPS, ServicoDeTempo
)
from motor_apolo.sistemas.inventario import Item
from motor_apolo.entidades.entidade import Personagem, Inimigo
from motor_apolo.ia.assistentes import (
    AssistenteSupervisionado, AssistenteReforco, AssistenteAutoSupervisionado
)

# ==============================================================================
# 2. FUNÇÃO PRINCIPAL E LOOP DE JOGO
# ==============================================================================

def main():
    """ Ponto de entrada principal do programa. """
    # --- Inicialização ---
    print("--- INICIALIZANDO O SISTEMA DE RPG (MOTOR APOLO) ---")
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

    # Gerando itens iniciais
    item_jogador = ia_autossupervisionada.gerar_item_aleatorio()
    jogador.inventario.adicionar_item(item_jogador)
    monstro.inventario.adicionar_item(Item("Poção de Cura Simples", "pocao"))

    # --- Início do Combate ---
    print("\n--- COMBATE INICIADO ---")
    print(f"{monstro.nome}: '{ia_supervisionada.gerar_dialogo('inicio_combate')}'\n")

    turno = 1
    while jogador.vida > 0 and monstro.vida > 0:
        print(f"--- TURNO {turno} ---")
        # --- Turno do Jogador ---
        print(f"--- Vez do Jogador (Vida: {jogador.vida}) ---")
        monstro.memoria.limpar_memoria_curto_prazo()

        acao_valida = False
        while not acao_valida:
            acao = input("O que você faz? (atacar / usar pocao): ").lower().strip()
            if acao == "atacar":
                jogador.atacar(monstro, sdf)
                acao_valida = True
            elif acao == "usar pocao":
                jogador.usar_pocao(sdf)
                acao_valida = True # A ação é válida mesmo que o jogador não tenha poção
            else:
                print("Ação inválida! Tente 'atacar' ou 'usar pocao'.")

        if monstro.vida <= 0:
            break

        # --- Turno do Inimigo ---
        print(f"\n--- Vez do Inimigo (Vida: {monstro.vida}) ---")
        acao_ia = monstro.assistente_ia.tomar_decisao_combate(monstro, jogador)
        if acao_ia == "atacar":
            monstro.atacar(jogador, sdf)
        elif acao_ia == "usar pocao":
            monstro.usar_pocao(sdf)

        print("-" * 25)
        turno += 1

    # --- Fim do Combate ---
    print("\n--- COMBATE FINALIZADO ---")
    if jogador.vida > 0:
        print(f"O {jogador.nome} foi vitorioso!")
        print(f"{monstro.nome}: '{ia_supervisionada.gerar_dialogo('fim_combate')}'")
    else:
        print(f"O {monstro.nome} foi vitorioso!")

if __name__ == "__main__":
    main()
